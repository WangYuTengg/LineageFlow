from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HelloWorldView(APIView):
    def get(self, request):
        return Response("Hello world", status=status.HTTP_200_OK)


class CreateRepositoryView(APIView):
    def post(self, request):
        # This is a placeholder for creating a repository
        return Response("Repository created", status=status.HTTP_201_CREATED)
