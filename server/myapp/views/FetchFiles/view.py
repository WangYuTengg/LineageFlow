from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Repo, Branch, Range, File, MetaRange
from django.db import DatabaseError
from myapp.gcs_utils import GCS 
from concurrent.futures import ThreadPoolExecutor, as_completed


class FetchLatestCommitDataView(APIView):  # Fixed the class name capitalization
    def get(self, request):
        repo_name = request.query_params.get('repo')
        branch_name = request.query_params.get('branch')
        
        if not repo_name or not branch_name: 
            return Response({"error": "Repo and branch names are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            repo = Repo.objects.get(repo_name=repo_name)
        except Repo.DoesNotExist:
            return Response({"error": "Repo not found"}, status=status.HTTP_404_NOT_FOUND)  # Fixed status typo
        except DatabaseError as e:
            return Response({"error": f"Database error while fetching repo: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try: 
            branch = Branch.objects.get(repo=repo, branch_name=branch_name)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            return Response({"error": f"Database error while fetching branch: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Fetch the latest commit for the branch
        latest_commit = branch.commits.first() 
        if not latest_commit:
            return Response({"error": "No commits found for this branch"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Fetch the MetaRange associated with the latest commit
            metarange = latest_commit.meta_range
            if not metarange:
                return Response({"error": "MetaRange not found for the latest commit"}, status=status.HTTP_404_NOT_FOUND)

            # Fetch all ranges associated with the MetaRange
            ranges = metarange.ranges.all()
            print("metarange_id:", metarange.meta_id)
            if not ranges.exists():
                return Response({"error": "No ranges found for the MetaRange"}, status=status.HTTP_404_NOT_FOUND)

            # Collect URLs of the files
            urls = []
            for range_obj in ranges:
                files = range_obj.files.all()
                if not files.exists():
                    return Response({"error": f"No files found in range {range_obj.range_id}"}, status=status.HTTP_404_NOT_FOUND)
                for file in files:
                    urls.append(file.url)

        except MetaRange.DoesNotExist:
            return Response({"error": "MetaRange not found"}, status=status.HTTP_404_NOT_FOUND)
        except Range.DoesNotExist:
            return Response({"error": "Range not found"}, status=status.HTTP_404_NOT_FOUND)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            return Response({"error": f"Database error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        gcs = GCS() 
        file_data = [] 
        
        try: 
            # Pull data from GCS for each file URL 
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(gcs.pull_data, url) for url in urls]
                for future in as_completed(futures):
                    try: 
                        data = future.result() 
                        file_data.append(data)
                    except Exception as e: 
                        return Response({"error": f"Error fetching data from GCS: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            return Response({"file_data": file_data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": f"Unexpected error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
