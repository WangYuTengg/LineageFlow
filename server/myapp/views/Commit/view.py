from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    CommitSerializer,
)
from myapp.models import (
    Commit,
)


class CommitView(APIView):
    def get(self, request):
        branch = request.query_params.get("branch_id")
        commits = Commit.objects.all().filter(branch_id=branch)
        print(commits)

        serializer = CommitSerializer(commits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
