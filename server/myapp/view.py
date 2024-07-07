from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RangeSerializer,
    CommitSerializer,
    BranchSerializer,
)
from .models import (
    MetaRange,
    Commit,
    Branch,
    Users,
)


class FilesView(APIView):
    def get(self, request):
        branch_id = request.query_params.get("branch_id")
        commit_obj = Branch.objects.get(branch_id=branch_id).commit_id
        meta = Commit.objects.get(commit_id=commit_obj.commit_id).meta_id
        ranges_obj = MetaRange.objects.get(meta_id=meta.meta_id).ranges
        # DEBUG
        # print(RangeSerializer(instance=ranges_obj, many=True))
        # files=Range.objects.filter(range_id__in=ranges_obj.all())
        serializer = RangeSerializer(instance=ranges_obj, many=True)
        if not serializer.data:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommitView(APIView):
    def get(self, request):
        branch = request.query_params.get("branch_id")
        commits = Commit.objects.all()
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
