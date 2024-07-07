from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    CommitSerializer,
    FilesSerializer,
)
from myapp.models import (
    Commit,
)


class CommitView(APIView):
    def get(self, request):
        branch = request.query_params.get("branch_id")
        commits = Commit.objects.all().filter(branch_id=branch)

        added_files = []
        removed_files = []
        modified_files = []

        for commit in commits:
            adds = commit.add.all()
            for add in adds:
                serializer = FilesSerializer(add)
                added_files.append(
                    {"file": serializer.data, "commit_id": commit.commit_id}
                )

            deletes = commit.remove.all()
            for delete in deletes:
                serializer = FilesSerializer(delete)
                removed_files.append(
                    {"file": serializer.data, "commit_id": commit.commit_id}
                )

            edits = commit.edit.all()
            for edit in edits:
                serializer = FilesSerializer(edit)
                modified_files.append(
                    {"file": serializer.data, "commit_id": commit.commit_id}
                )

        serializer = CommitSerializer(commits, many=True)

        return Response(
            {
                "commits": serializer.data,
                "adds": added_files,
                "deletes": removed_files,
                "edits": modified_files,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        repo_name = request.data.get("repo_name")
        branch = request.data.get("branch")
        file = request.FILES.get("file")

        serializer = CommitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
