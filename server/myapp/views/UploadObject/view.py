from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from myapp.models import Branch, Repo, Range, Commit, MetaRange, File
from myapp.serializers import FilesSerializer
from myapp.gcs_utils import GCS
from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.exceptions import ValidationError
import json

class UploadObjectView(APIView):
    def post(self, request):
        repo_name = request.data.get('repo')
        branch_name = request.data.get('branch')
        files = request.FILES.getlist('files')
        relative_paths = request.data.getlist('relative_paths')
        storage_bucket = request.data.get('storage_bucket')

        try:
            repo = Repo.objects.get(repo_name=repo_name)
        except Repo.DoesNotExist:
            return Response({"error": "Repo not found"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            return Response({"error": f"Database error while fetching repo: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            branch = Branch.objects.get(repo=repo, branch_name=branch_name)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            return Response({"error": f"Database error while fetching branch: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        gcs = GCS()

        if not files:
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            object_metadata = []
            new_files = []
            edited_files = []

            with ThreadPoolExecutor() as executor:
                futures = []
                for file, relative_path in zip(files, relative_paths):
                    existing_file = File.objects.filter(url__startswith=relative_path).first()
                    if existing_file:
                        edited_files.append(existing_file)
                        version = existing_file.version + 1
                    else:
                        version = 1
                    futures.append(executor.submit(gcs.upload_and_get_metadata, file, relative_path, storage_bucket, version))

                for future in as_completed(futures):
                    try:
                        file_obj = future.result()
                        object_metadata.append(file_obj)
                    except ValueError as ve:
                        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        print(f"Error occurred during file upload and metadata retrieval: {e}")
                        return Response({"error": f"File upload error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with transaction.atomic():
                latest_commit = branch.commits.first()
                new_metarange = MetaRange.objects.create()
                print(f"New MetaRange created: {new_metarange.meta_id}")

                if not latest_commit:
                    # No existing commits, create new MetaRange and Range objects
                    ranges = gcs.group_into_ranges(object_metadata)
                    
                    for range_subset in ranges: 
                        new_range = Range.objects.create()
                        
                        for url, metadata in range_subset.items():
                            try:
                                new_file_instance = File.objects.create(
                                    url=url,
                                    meta_data=json.dumps(metadata),
                                    range=new_range,
                                    metarange=new_metarange
                                )
                                print(f"New File created: {new_file_instance.url}, MetaRange: {new_file_instance.metarange.meta_id}")
                                new_files.append(new_file_instance)
                            except IntegrityError as e:
                                print(f"Integrity error while saving new file: {e}")
                                return Response({"error": f"Integrity error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except DatabaseError as e:
                                print(f"Database error while saving new file: {e}")
                                return Response({"error": f"Database error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                        new_metarange.ranges.add(new_range)
                        print(f"New range added to MetaRange: {new_range.range_id}")

                    new_metarange.save()

                    new_commit = Commit.objects.create(
                        branch=branch,
                        created_timestamp=timezone.now(),
                        meta_range=new_metarange
                    )
                    new_commit.add.set(new_files)
                    new_commit.save()
                    print(f"New commit created: {new_commit.commit_id}")
                    
                else:
                    metarange = latest_commit.meta_range
                    existing_ranges = list(metarange.ranges.all())
                    updated_ranges = existing_ranges.copy()
                    processed_ranges = {}

                    for file_data in object_metadata:
                        files_serializer = FilesSerializer(data=file_data)
                        if files_serializer.is_valid():
                            try:
                                existing_file = next((f for f in edited_files if f.url == file_data['url']), None)
                                if existing_file:
                                    existing_file.version += 1
                                    existing_file.meta_data = file_data['meta_data']
                                    existing_file.metarange = new_metarange
                                    print(f"Before save - Updated File: {existing_file.url}, MetaRange: {existing_file.metarange.meta_id}")
                                    existing_file.save()
                                    print(f"After save - Updated File: {existing_file.url}, MetaRange: {existing_file.metarange.meta_id}")

                                    old_range = existing_file.range
                                    if old_range in processed_ranges:
                                        new_range_excluding_edited = processed_ranges[old_range]
                                    else:
                                        old_range_files = list(old_range.files.all())
                                        old_range_files.remove(existing_file)
                                        new_range_excluding_edited = Range.objects.create()
                                        new_range_excluding_edited.files.set(old_range_files)
                                        processed_ranges[old_range] = new_range_excluding_edited

                                    updated_ranges = [r for r in updated_ranges if r != old_range]
                                    updated_ranges.append(new_range_excluding_edited)
                                    print(f"Range {old_range.range_id} processed and replaced with {new_range_excluding_edited.range_id}")

                                else:
                                    new_file_instance = files_serializer.save()
                                    new_file_instance.range = new_range
                                    new_file_instance.metarange = new_metarange
                                    new_file_instance.save()
                                    print(f"New File created in existing commit: {new_file_instance.url}, MetaRange: {new_file_instance.metarange.meta_id}")
                                    new_files.append(new_file_instance)
                            except IntegrityError as e:
                                print(f"Integrity error while saving file: {e}")
                                return Response({"error": f"Integrity error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except DatabaseError as e:
                                print(f"Database error while saving file: {e}")
                                return Response({"error": f"Database error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            print(f"Serializer errors: {files_serializer.errors}")
                            return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    new_meta_obj = MetaRange.objects.create()
                    new_meta_obj.ranges.set(updated_ranges)
                    new_meta_obj.save()
                    print(f"Updated MetaRange created: {new_meta_obj.meta_id}")

                    new_commit = Commit.objects.create(
                        branch=branch,
                        created_timestamp=timezone.now(),
                        meta_range=new_meta_obj
                    )
                    new_commit.add.set(new_files)
                    new_commit.edit.set(edited_files)
                    new_commit.save()
                    print(f"New Commit created: {new_commit.commit_id}")

            return Response({"commit_id": new_commit.commit_id}, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            print(f"Validation error: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
