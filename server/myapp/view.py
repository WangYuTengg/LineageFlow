from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RepositorySerializer,
    ItemSerializer,
    FilesSerializer,
    RangeSerializer,
    MetaRangeSerializer,
    CommitSerializer,
    BranchSerializer,
)
from django.db import connection
from .models import Item, Range, MetaRange, Commit, Branch


class HelloWorldView(APIView):
    def get(self, request):
        return Response("Hello world", status=status.HTTP_200_OK)


class CreateRepositoryView(APIView):
    def post(self, request):
        serializer = RepositorySerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# testing on the cloud db
class TestView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RangeView(APIView):
    def get(self, request):
        ranges = Range.objects.all()
        serializer = RangeSerializer(ranges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetaView(APIView):
    def get(self, request):
        metas = MetaRange.objects.all()
        serializer = MetaRangeSerializer(metas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MetaRangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommitView(APIView):
    def get(self, request):
        commits = Commit.objects.all()
        serializer = CommitSerializer(commits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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
    def get(self, request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Data Inserted Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAdminView(APIView):
    def post(self, request):
        if (
            request.data.get("username") == "admin"
            and request.data.get("password") == "admin"
        ):
            return Response(request.data, status=status.HTTP_200_OK)
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
