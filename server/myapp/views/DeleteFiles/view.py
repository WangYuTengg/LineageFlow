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
from django.shortcuts import get_object_or_404

class DeleteFile(APIView):
    def post(self, request):
        urls_to_delete = request.data.getlist('files_list')
        repo_name = request.data.get('repo')
        branch_name = request.data.get('branch')
        
        if len(urls_to_delete) < 1:
            return Response({"error": "No files to delete"}, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        storage_bucket = repo.bucket_url
        gcs = GCS()
        
        updated_ranges = []
        processed_ranges = {}
        
        latest_commit = branch.commits.first()
        
        latest_metarange = latest_commit.meta_range
        
        with transaction.atomic():
            for url in urls_to_delete:
                file_instance = get_object_or_404(File, url=url)
                old_range = file_instance.range
                
                if old_range in processed_ranges:
                    new_range_excluding_removed = processed_ranges[old_range]
                    new_range_excluding_removed.remove(file_instance)
                    processed_ranges[old_range] = new_range_excluding_removed

                else:
                    old_range_files = list(old_range.files.all())
                    old_range_files.remove(file_instance)
                    
                    new_range_excluding_removed = Range.objects.create()
                    new_range_excluding_removed.files.set(old_range_files)
                    
                    processed_ranges[old_range] = new_range_excluding_removed

                updated_ranges = [r for r in latest_metarange.ranges.all() if r != old_range]
                updated_ranges.append(new_range_excluding_removed)
                
                # Delete the file from the GCS bucket
                try:
                    gcs.delete_file(storage_bucket, url)
                except Exception as e:
                    return Response({"error": f"Error deleting file from GCS: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            latest_metarange.ranges.set(updated_ranges)
            latest_metarange.save()

            # Create a new commit
            new_commit = Commit.objects.create(
                branch=branch,
                created_timestamp=timezone.now()
            )
            new_commit.remove.set(File.objects.filter(url__in=urls_to_delete))
            new_commit.save()

            latest_metarange.commit = new_commit
            latest_metarange.save()

        return Response({"commit_id": new_commit.commit_id}, status=status.HTTP_201_CREATED)
