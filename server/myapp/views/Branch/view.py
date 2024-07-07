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


class BranchView(APIView):
    def post(self, request):
        # sample post req: {"username": "admin", "repo_name": "TEST", "parent": "main", "branch_name": "newB"}
        username = request.data.pop("username")
        repo = request.data.pop("repo_name")
        parent = request.data.pop("parent")

        repo_list = Users.objects.get(username=username).repos
        repo_id = repo_list.get(repo_name=repo)

        # the new branch will point to that commit
        old_commit = Branch.objects.get(repo_id=repo_id, branch_name=parent).commit_id
        new_branch = Branch.objects.create(
            branch_name=request.data.get("branch_name"),
            commit_id=old_commit,
            repo_id=repo_id,
        )
        serializer = BranchSerializer(instance=new_branch)
        response_data = {
            "message": "Branch Created Successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
