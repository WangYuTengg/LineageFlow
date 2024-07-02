from myapp.serializers import FilesSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from myapp.models import Files
from .gcs_utils import GCS

gcs = GCS() 
class OnboardingView(APIView):
    def get(self,request):
        files = Files.objects.all() #change according to whtv condition
        serializer = FilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            bucket_url = serializer.data.bucket_url
            objects = gcs.list_gcs_objects(bucket_url)
            ranges = gcs.group_into_ranges(objects)
            
            for i, range_group in enumerate(ranges):
                print(f"Range {i + 1}:")
                for object_pointer, metadata in range_group.items():
                    print(f"  {object_pointer}: {metadata}")
                print()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)