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
        file = request.FILES.get('file')
        storage_bucket = request.data.get('storage_bucket')
        
        # repo is an object that contains repo.repo_id and repo.repo_name
        repo = Repo.objects.get(repo_name = repo_name)
        
        print(repo.repo_id)
        
        branch = Branch.objects.get(repo_id = repo.repo_id, branch_name = branch)
        print(branch.branch_id)
        
        gcs = GCS() 
        #change this later
        object_metadata = []
        
        if file:
            file_paths = [] 
            if hasattr(file, 'path') and os.path.isdir(file.path):
                # it is a folder 
                for root, _ , files in os.walk(file.path):
                    for filename in files: 
                        relative_path = os.path.relpath(os.path.join(root, filename), file.path)
                        file_paths.append(relative_path)
                    
            else: 
                # it is a single file 
                file_paths.append(file.name)  
                
            return Response(file_paths, status=status.HTTP_200_OK)
                
                      
        return Response(branch, status=status.HTTP_200_OK)
        
  

        

                
        #     for path in file_paths:
        #         url = f"https://storage.googleapis.com/techjam/{path}"
        #         # check if the URL already exists in the Range table 
        #         if Range.objects.filter(metarange_id = meta_id, url = url).exists():
        #             # file is being updated or removed 
        #             # handle update or remove logic here 
                    
        #             return 
                
        #         else: 
        #             with open(os.path.join(file.path, path), 'rb') as f: 
        #                 gcs.upload_to_gcs(f, path, bucket_link=bucket_link)
        #             metadata = gcs.get_file_metadata(bucket_link, path)
        #             object_metadata.append({url: metadata})

        #         if '/' in path: 
        #             # it is a file within a folder 
                    