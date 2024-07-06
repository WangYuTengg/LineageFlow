from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    FilesSerializer,
)
from myapp.models import Branch, Commit, MetaRange, Range, File


class GetObjectsView(APIView):
    def get(self, request):
        repo_id = request.query_params.get("id")
        branch_name = request.query_params.get("branch")
        branch = Branch.objects.get(repo_id=repo_id, branch_name=branch_name)

        commits = Commit.objects.filter(branch=branch)
        # Initial commit might not exist
        if not commits.exists():
            return Response({"files": []}, status=status.HTTP_200_OK)

        latest_commit = commits.first()  # return latest commit
        print("latest_commit:", latest_commit)
        meta_range = MetaRange.objects.get(commit=latest_commit)
        ranges = meta_range.ranges.all()
        kvs = []
        for range in ranges:
            files = range.files.all()
            serializer = FilesSerializer(files, many=True)
            kvs.append(serializer.data)

        return Response({"files": kvs}, status=status.HTTP_200_OK)
