from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    FilesSerializer,
)
from myapp.models import (
    Branch,
)


class GetObjectsView(APIView):
    def get(self, request):
        repo_id = request.query_params.get("id")
        branch_name = request.query_params.get("branch")
        branch = Branch.objects.get(repo_id=repo_id, branch_name=branch_name)

        # Have to do it this way as branch might not have a commit_id (especially after /onboard)
        try:
            commit = branch.commit_id
            metarange = commit.meta_id
            ranges = metarange.ranges.all()
            kvs = []
            for range in ranges:
                files = range.files.all()
                serializer = FilesSerializer(files, many=True)
                kvs.append(serializer.data)

            return Response({"files": kvs}, status=status.HTTP_200_OK)

        except:
            return Response({"files": []}, status=status.HTTP_200_OK)
