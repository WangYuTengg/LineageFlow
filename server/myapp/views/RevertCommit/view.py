from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Commit, MetaRange
from django.db import transaction

class RevertCommit(APIView):
    def get(self, request):
        current_commit_id = request.query_params.get("commit")
        target_commit_id = request.query_params.get("target_commit")

        if not current_commit_id or not target_commit_id:
            return Response({"error": "Both current commit and target commit must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_commit = Commit.objects.get(commit_id=current_commit_id)
            target_commit = Commit.objects.get(commit_id=target_commit_id)
        except Commit.DoesNotExist:
            return Response({"error": "Current commit or target commit not found"}, status=status.HTTP_404_NOT_FOUND)

        if current_commit.branch != target_commit.branch:
            return Response({"error": "Commits are not in the same branch"}, status=status.HTTP_400_BAD_REQUEST)

        target_commit_metarange = target_commit.meta_range
        target_commit_metarange_ranges = target_commit_metarange.ranges.all()

        with transaction.atomic():
            new_metarange = MetaRange.objects.create()
            new_metarange.ranges.add(*target_commit_metarange_ranges)

            new_commit = Commit.objects.create(
                branch=current_commit.branch,
                commit_message="Rollback to commit {}".format(target_commit.commit_id)
            )

            new_metarange.commit = new_commit
            new_metarange.save()

        return Response({
            "target_commit_id": target_commit.commit_id,
            "target_commit_message": target_commit.commit_message,
            "target_commit_timestamp": target_commit.created_timestamp,
            "new_commit_id": new_commit.commit_id
        }, status=status.HTTP_200_OK)
