from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from myapp.models import Branch, Repo, Range, Commit, MetaRange
from myapp.serializers import CommitSerializer, FilesSerializer, RangeSerializer, MetaRangeSerializer
from myapp.gcs_utils import GCS
from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.exceptions import ValidationError

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
            branch = Branch.objects.get(repo_id=repo.repo_id, branch_name=branch_name)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            return Response({"error": f"Database error while fetching branch: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        gcs = GCS()

        if not files:
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            object_metadata = []
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(gcs.upload_and_get_metadata, file, relative_path, storage_bucket)
                    for file, relative_path in zip(files, relative_paths)
                ]

                for future in as_completed(futures):
                    try:
                        file_obj = future.result()
                        object_metadata.append(file_obj)
                    except Exception as e:
                        print(f"Error occurred during file upload and metadata retrieval: {e}")
                        return Response({"error": f"File upload error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            file_instances = []
            for file_data in object_metadata:
                files_serializer = FilesSerializer(data=file_data)
                if files_serializer.is_valid():
                    try:
                        file_instance = files_serializer.save()
                        file_instances.append(file_instance)
                    except IntegrityError as e:
                        return Response({"error": f"Integrity error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except DatabaseError as e:
                        return Response({"error": f"Database error while saving file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                try:
                    new_range = Range.objects.create()
                except IntegrityError as e:
                    return Response({"error": f"Integrity error while creating range: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError as e:
                    return Response({"error": f"Database error while creating range: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    new_range.files.set(file_instances)
                except IntegrityError as e:
                    return Response({"error": f"Integrity error while setting files for range: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError as e:
                    return Response({"error": f"Database error while setting files for range: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    latest_commit = branch.commit_id
                except DatabaseError as e:
                    return Response({"error": f"Database error while fetching latest commit: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    metarange = latest_commit.meta_id
                except AttributeError:
                    return Response({"error": "Latest commit does not have a metarange"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    meta_obj = MetaRange.objects.get(meta_id=metarange.meta_id)
                except MetaRange.DoesNotExist:
                    return Response({"error": "MetaRange not found"}, status=status.HTTP_404_NOT_FOUND)
                except DatabaseError as e:
                    return Response({"error": f"Database error while fetching MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    meta_obj.ranges.add(new_range)
                    meta_obj.save()
                except IntegrityError as e:
                    return Response({"error": f"Integrity error while adding range to MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError as e:
                    return Response({"error": f"Database error while saving MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    new_meta_obj = MetaRange.objects.create()
                    new_meta_obj.ranges.set(meta_obj.ranges.all())
                    new_meta_obj.ranges.add(new_range)
                    new_meta_obj.save()
                except IntegrityError as e:
                    return Response({"error": f"Integrity error while creating new MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError as e:
                    return Response({"error": f"Database error while creating new MetaRange: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                try:
                    new_commit = Commit.objects.create(
                        meta_id=new_meta_obj,
                        timestamp=timezone.now()
                    )
                except IntegrityError as e:
                    return Response({"error": f"Integrity error while creating new commit: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError as e:
                    return Response({"error": f"Database error while creating new commit: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"commit_id": new_commit.commit_id}, status=status.HTTP_201_CREATED)
        
        except ValidationError as ve:
            print(f"Validation error: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
