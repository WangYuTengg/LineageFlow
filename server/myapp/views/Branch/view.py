from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from myapp.models import (
    Repo,
    Branch,
    Commit,
    MetaRange,
)


class BranchView(APIView):
    def post(self, request):
        # sample post req: {"username": "admin", "repo_name": "TEST", "parent": "main", "branch_name": "newB"}
        repo_id = request.data.get("repo_id")
        parent_branch = request.data.get("parent_branch")
        branch_name = request.data.get("branch_name")
        print("Received request data:", request.data)

        source_repo = Repo.objects.get(repo_id=repo_id)
        print("Source repo found:", source_repo)

        source_branch = Branch.objects.get(repo_id=repo_id, branch_name=parent_branch)
        print("Source branch found:", source_branch)

        source_commit = (
            Commit.objects.filter(branch=source_branch)
            .order_by("-created_timestamp")
            .first()
        )
        print("Source commit found:", source_commit)

        source_metarange = MetaRange.objects.get(commit=source_commit)
        print("Source metarange found:", source_metarange)

        with transaction.atomic():
            # create new branch
            new_branch = Branch.objects.create(
                branch_name=branch_name,
                repo=source_repo,
            )
            print("New branch created:", new_branch)

            # create new commit for new branch
            new_commit = Commit.objects.create(
                branch=new_branch,
                commit_message=f"New branch created from {parent_branch} branch.",
            )
            print("New commit created:", new_commit)

            # create new meta range for new commit
            new_meta_range = MetaRange.objects.create()
            print("New meta range created:", new_meta_range)

            new_meta_range.ranges.add(*source_metarange.ranges.all())
            print("Ranges added to new meta range:", new_meta_range.ranges.all())

            new_branch.save()
            new_commit.save()
            new_meta_range.save()

        return Response(
            {
                "message": "Branch Created Successfully",
            },
            status=status.HTTP_201_CREATED,
        )
