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
    UserSerializer,
    RoleSerializer,
)
from .models import Item, Range, MetaRange, Commit, Branch, Users, UserToRepo, Repo


class HelloWorldView(APIView):
    def get(self, request):
        return Response("Hello world", status=status.HTTP_200_OK)


class CreateRepositoryView(APIView):
    def post(self, request):
        """request body needs username, repo name, default branch name
        optional: bucket_url, description"""

        username = request.data.pop("username")
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        repo_instance = RepositorySerializer(data=request.data)
        if repo_instance.is_valid():
            repo_instance.save()
            repo = Repo.objects.get(**repo_instance.validated_data)
            user.repos.add(repo)
            user_instance = UserSerializer(instance=user)
            # TODO create the usertorepo
            response_data = {
                "message": "Repo Created Successfully",
                "data": repo_instance.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", repo_instance.errors)
        return Response(repo_instance.errors, status=status.HTTP_400_BAD_REQUEST)


# testing on the cloud db
# class TestView(APIView):
#     def get(self, request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 "message": "Data Inserted Successfully",
#                 "data": serializer.data,
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def get(self, request):
        username = request.query_params.get("username")
        repo = request.query_params.get("repo_name")
        try:
            repo_list = Users.objects.get(username=username).repos
        except Users.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            repo_instance = repo_list.get(repo_name=repo)
        except Repo.DoesNotExist:
            return Response(
                {"error": "Repository not found"}, status=status.HTTP_404_NOT_FOUND
            )

        branches = Branch.objects.filter(repo_id=repo_instance)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Branch Created Successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAdminView(APIView):
    def post(self, request):
        username = request.data.get("username")
        pw = request.data.get("password")
        # TODO; include the hashing later on
        user = Users.objects.filter(username=username).values("password", "repos")
        if user[0].get("password") == pw:
            response_data = {"message": "Login Successfully", "data": user[0]}
        else:
            response_data = {"message": "Invalid credentials"}
        return Response(response_data, status=status.HTTP_200_OK)


class CreateUserView(APIView):
    def post(self, request):
        user_instance = UserSerializer(data=request.data)
        if user_instance.is_valid():
            user_instance.save()
            response_data = {
                "message": "User Created Successfully!",
                "data": user_instance.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(user_instance.errors, status=status.HTTP_401_UNAUTHORIZED)
