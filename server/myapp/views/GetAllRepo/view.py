from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    BranchSerializer,
)
from myapp.models import (
    Branch,
    Users,
)


class GetRepoView(APIView):
    def get(self, request):
        username = request.query_params.get("username")
        if not username:
            return Response(
                {"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        repos = user.repos.all()

        response_data = []
        for repo in repos:
            repo_data = {
                "repo_id": repo.repo_id,
                "repo_name": repo.repo_name,
                "default_branch": repo.default_branch,
                "description": repo.description,
                "bucket_url": repo.bucket_url,
                "created_timestamp": repo.created_timestamp,
                "updated_timestamp": repo.updated_timestamp,
                "branches": [],
            }

            branches = Branch.objects.filter(repo=repo)
            for branch in branches:
                branch_data = BranchSerializer(branch).data
                latest_commit = branch.commits.order_by("-created_timestamp").first()
                branch_data["latest_commit"] = (
                    {
                        "commit_id": latest_commit.commit_id,
                        "commit_message": latest_commit.commit_message,
                        "created_timestamp": latest_commit.created_timestamp,
                    }
                    if latest_commit
                    else None
                )
                repo_data["branches"].append(branch_data)

            response_data.append(repo_data)

        return Response(response_data, status=status.HTTP_200_OK)
