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
                # Check if there are existing commits for the branch
                latest_commit = branch.commits.first()
                new_metarange = MetaRange.objects.create()

                if not latest_commit:
                    # No existing commits, create new MetaRange and Range objects

                    # get list of ranges 
                    # iterate through each key value pair and append it to range object
                    # Group the objects metadata into ranges
                    # Group the objects metadata into ranges
                    ranges = gcs.group_into_ranges(object_metadata)
                    
                    print(ranges)

                    # Iterate through each range (subset) and create Range objects
                    for range_subset in ranges: 
                        new_range = Range.objects.create()
                        
                        # Iterate through each key-value pair in the range subset
                        for url, metadata in range_subset.items():
                            try:
                                # Create a new File instance and associate it with the new Range
                                new_file_instance = File.objects.create(
                                    url=url,
                                    meta_data=json.dumps(metadata),
                                    range=new_range
                                )
                                new_files.append(new_file_instance)
                            except IntegrityError as e:
                                return Response({"error": f"Integrity error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except DatabaseError as e:
                                return Response({"error": f"Database error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                        # Add the new Range object to the MetaRange
                        new_metarange.ranges.add(new_range)

                    # Save the MetaRange to persist changes
                    new_metarange.save()

                    # Create new commit associated with the new MetaRange
                    new_commit = Commit.objects.create(
                        branch=branch,
                        created_timestamp=timezone.now()
                    )
                    new_commit.add.set(new_files)
                    new_commit.save()
                    
                    new_metarange.commit = new_commit 
                    new_metarange.save()

                else:
                    # Existing commits found, use the latest commit's MetaRange
                    try: 
                        metarange = latest_commit.meta_range
                    except MetaRange.DoesNotExist:
                        return Response({"error": "MetaRange not found"}, status=status.HTTP_404_NOT_FOUND)
                    except DatabaseError as e:
                        return Response({"error": f"Database error while fetching MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    new_range = Range.objects.create()
                    existing_ranges = list(metarange.ranges.all())
                    updated_ranges = []
                    processed_ranges = {}

                    # Process files
                    for file_data in object_metadata:
                        files_serializer = FilesSerializer(data=file_data)
                        if files_serializer.is_valid():
                            try:
                                existing_file = File.objects.filter(url=file_data['url']).first()
                                if existing_file:
                                    # Handle edited file
                                    existing_file.version += 1
                                    existing_file.meta_data = file_data['meta_data']
                                    existing_file.save()
                                    edited_files.append(existing_file)

                                    old_range = existing_file.range
                                    if old_range in processed_ranges:
                                        # If the range has already been processed, get the new range from the processed_ranges dictionary
                                        new_range_excluding_edited = processed_ranges[old_range]
                                    else:
                                        # Duplicate the range
                                        old_range_files = list(old_range.files.all())

                                        # Remove edited file from the old range files
                                        old_range_files.remove(existing_file)

                                        # Create a new range and add the files excluding the edited file
                                        new_range_excluding_edited = Range.objects.create()
                                        new_range_excluding_edited.files.set(old_range_files)

                                        # Mark this range as processed
                                        processed_ranges[old_range] = new_range_excluding_edited

                                    # Exclude the old range from meta_obj and add the new ranges
                                    updated_ranges = [r for r in existing_ranges if r != old_range]

                                    updated_ranges.append(new_range_excluding_edited)

                                else:
                                    new_file_instance = files_serializer.save()
                                    new_file_instance.range = new_range
                                    new_file_instance.save()
                                    new_files.append(new_file_instance)
                            except IntegrityError as e:
                                return Response({"error": f"Integrity error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            except DatabaseError as e:
                                return Response({"error": f"Database error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # Create new MetaRange with updated ranges
                    new_meta_obj = MetaRange.objects.create()
                    new_meta_obj.ranges.set(updated_ranges)
                    new_meta_obj.save()

                    # Create a new commit with the updated MetaRange
                    new_commit = Commit.objects.create(
                        branch=branch,
                        created_timestamp=timezone.now()
                    )
                    new_commit.add.set(new_files)
                    new_commit.edit.set(edited_files)
                    new_commit.save()
                    
                    new_meta_obj.commit = new_commit 
                    new_meta_obj.save()

            return Response({"commit_id": new_commit.commit_id}, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            print(f"Validation error: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
