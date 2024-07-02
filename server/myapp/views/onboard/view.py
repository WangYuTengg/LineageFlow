from myapp.serializers import FilesSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from myapp.models import Files
from .gcs_utils import GCS
from .serializer import BucketRequestSerializer

gcs = GCS() 
class OnboardingView(APIView):
    def get(self,request):
        files = Files.objects.all() #change according to whtv condition
        serializer = FilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = BucketRequestSerializer(data = request.data)
        if serializer.is_valid():   
            bucket_url = request.data.get("bucket_url")
            objects = gcs.list_gcs_objects(bucket_url)
            ranges = gcs.group_into_ranges(objects)
            return Response(ranges, status = status.HTTP_201_CREATED)

        else:
            return Response(serializer.erros, status = status.HTTP_400_BAD_REQUEST)
