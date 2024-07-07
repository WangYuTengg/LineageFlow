from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from myapp.models import Branch, Repo, Range, Commit, MetaRange, File
from myapp.gcs_utils import GCS
from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class DeleteFile(APIView):
    
    """
        file = {
            "file_name":
            "id": 
            "loc":
            "metadata" : 
            "range":  
        }
    """
    def post(self, request):
        files = request.data.getlist('files_list')
        repo_name = request.data.get('repo')
        branch_name = request.data.get('branch')
        
        repo = self.get_repo(repo_name)
        branch = self.get_branch(repo, branch_name)

        latest_commit = Commit.objects.filter(branch=branch).order_by('-created_timestamp').first()
        metarange = latest_commit.meta_range
        all_ranges = list(metarange.ranges.all())
        
        files_to_delete = []

        for file in files: 
            target_range = file["range"]
            all_ranges.remove(target_range)
            files_to_delete.append(file)
            
        try:
            self.create_metarange_and_commit(branch, all_ranges, files_to_delete)
            return Response({"message": "Files deleted successfully."}, status=status.HTTP_200_OK)
        except (IntegrityError, DatabaseError) as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            
    def get_repo(self, repo_name):
        try:
            repo = Repo.objects.get(repo_name=repo_name)
            print(f'Found repo: {repo_name}')
            return repo
        except Repo.DoesNotExist:
            print(f'Repository "{repo_name}" not found')
            raise ValidationError(f"Repository '{repo_name}' not found")
    
    def get_branch(self, repo, branch_name):
        try:
            branch = Branch.objects.get(repo=repo, branch_name=branch_name)
            print(f'Found branch: {branch_name} in repo: {repo.repo_name}')
            return branch
        except Branch.DoesNotExist:
            print(f'Branch "{branch_name}" not found in repository "{repo.repo_name}"')
            raise ValidationError(f"Branch '{branch_name}' not found in repository '{repo.repo_name}'")
        
    def create_metarange_and_commit(self, branch, list_of_range_objects, list_of_file_obj_delete=[]):
        with transaction.atomic():
            print('Creating MetaRange and Commit')
            new_metarange = MetaRange.objects.create()
            new_metarange.ranges.add(*list_of_range_objects)

            # Create the commit without linking the meta_range initially
            new_commit = Commit.objects.create(
                branch=branch,
                commit_message="Auto-generated commit"  # Add a default message or adjust as necessary
            )

            # Link the meta_range to the commit
            new_metarange.commit = new_commit
            new_metarange.save()
            
            new_commit.remove.add(*list_of_file_obj_delete)
            new_commit.save()

 
