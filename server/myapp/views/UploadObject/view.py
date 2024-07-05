from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from myapp.models import Branch, Repo, Range
from myapp.gcs_utils import GCS
import os
class UploadObjectView(APIView):
    def post(self, request):
        repo_name = request.data.get('repo')
        branch = request.data.get('branch')
        
        files = request.FILES.getlist('files')
        relative_paths = request.data.getlist('relative_paths')
        
        storage_bucket = request.data.get('storage_bucket')
            
        print(storage_bucket)
        
        try:
            repo = Repo.objects.get(repo_name=repo_name)
        except Repo.DoesNotExist:
            return Response({"error": "Repo not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the branch object
        try:
            branch = Branch.objects.get(repo_id=repo.repo_id, branch_name=branch)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        
        gcs = GCS() 
        #change this later
        object_metadata = []
        
        if files:
            for file, relative_path in zip(files, relative_paths):
                public_url = gcs.upload_to_gcs(file, relative_path, storage_bucket)
                metadata = gcs.get_file_metadata(storage_bucket, relative_path)
                file_obj = {
                    public_url: metadata
                }
                object_metadata.append(file_obj)

            object_metadata.sort(key = lambda x: list(x.keys())[0])
            ranges = gcs.group_into_ranges(object_metadata)
            print(ranges)

        return Response(branch.branch_id, status=status.HTTP_200_OK)
        
        
  