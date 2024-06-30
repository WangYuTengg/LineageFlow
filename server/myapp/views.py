from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RepositorySerializer
from django.db import connection


class HelloWorldView(APIView):
    def get(self, request):
        return Response("Hello world", status=status.HTTP_200_OK)


class CreateRepositoryView(APIView):
    def post(self, request):
        serializer = RepositorySerializer(data=request.data)
        if serializer.is_valid():
            # data = serializer.save()
            response_data = {
                "message": "Repository created successfully",
                "repository_data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# testing on the cloud db
class TestView(APIView):
    def get(self,request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM test")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
        return Response(result, status=status.HTTP_201_OK)