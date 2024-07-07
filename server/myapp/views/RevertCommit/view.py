from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Commit, MetaRange
from django.db import transaction

class RevertCommit(APIView):
    def get(self, request):
        branch_id = request.query_params.get("branch_id")
        current_commit_id = request.query_params.get("commit")

        try:
            current_commit = Commit.objects.get(commit_id=current_commit_id, branch_id=branch_id)
        except Commit.DoesNotExist:
            return Response({"error": "Current commit not found"}, status=status.HTTP_404_NOT_FOUND)

        commits = Commit.objects.filter(branch_id=branch_id).order_by('-created_timestamp')

        try:
            current_index = list(commits).index(current_commit)
            previous_commit = commits[current_index + 1] if current_index + 1 < len(commits) else None
        except ValueError:
            return Response({"error": "Current commit is not in the commit list"}, status=status.HTTP_400_BAD_REQUEST)

        if not previous_commit:
            return Response({"message": "No previous commit found"}, status=status.HTTP_200_OK)

        previous_metarange = previous_commit.meta_range
        previous_metarange_ranges = previous_metarange.ranges.all()

        with transaction.atomic():
            new_metarange = MetaRange.objects.create() 
            new_metarange.ranges.add(*previous_metarange_ranges)
            
            new_commit = Commit.objects.create(
                branch=current_commit.branch,
                commit_message="Rollback of commit {}".format(current_commit.commit_id)
            )
            
            new_metarange.commit = new_commit
            new_metarange.save()

        return Response({
            "previous_commit_id": previous_commit.commit_id,
            "previous_commit_message": previous_commit.commit_message,
            "previous_commit_timestamp": previous_commit.created_timestamp,
            "new_commit_id": new_commit.commit_id
        }, status=status.HTTP_200_OK)