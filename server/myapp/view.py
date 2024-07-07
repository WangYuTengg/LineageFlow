from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RangeSerializer,
)
from .models import (
    MetaRange,
    Commit,
    Branch,
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
