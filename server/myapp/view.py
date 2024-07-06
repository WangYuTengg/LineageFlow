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
from .models import (
    Item,
    Range,
    MetaRange,
    Commit,
    Branch,
    Users,
    UserToRepo,
    Repo,
    Files,
)


class CreateRepositoryView(APIView):
    def post(self, request):
        #{"username": "admin", "repo_name": "ADMIN", "default_branch": "master"}

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


# class RangeView(APIView):
#     def get(self, request):
#         ranges = Range.objects.all()
#         serializer = RangeSerializer(ranges, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = RangeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 "message": "Data Inserted Successfully",
#                 "data": serializer.data,
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MetaView(APIView):
#     def get(self, request):
#         metas = MetaRange.objects.all()
#         serializer = MetaRangeSerializer(metas, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = MetaRangeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 "message": "Data Inserted Successfully",
#                 "data": serializer.data,
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilesView(APIView):
    def get(self, request):
        branch_id=request.query_params.get("branch_id")
        commit_obj=Branch.objects.get(branch_id=branch_id).commit_id
        meta=Commit.objects.get(commit_id=commit_obj.commit_id).meta_id
        ranges_obj=MetaRange.objects.get(meta_id=meta.meta_id).ranges
        # DEBUG
        # print(RangeSerializer(instance=ranges_obj, many=True))
        # files=Range.objects.filter(range_id__in=ranges_obj.all())
        serializer = RangeSerializer(instance=ranges_obj, many=True)
        if (not serializer.data):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
         
            

class CommitView(APIView):
    def get(self, request):
        branch = request.query_params.get("branch_id")
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
    def post(self, request):
        # sample post req: {"username": "admin", "repo_name": "TEST", "parent": "main", "branch_name": "newB"}
        username = request.data.pop("username")
        repo = request.data.pop("repo_name")
        parent = request.data.pop("parent")

        repo_list = Users.objects.get(username=username).repos
        repo_id = repo_list.get(repo_name=repo)

        # the new branch will point to that commit
        old_commit = Branch.objects.get(repo_id=repo_id, branch_name=parent).commit_id
        new_branch = Branch.objects.create(
            branch_name=request.data.get("branch_name"),
            commit_id=old_commit,
            repo_id=repo_id)
        serializer = BranchSerializer(instance=new_branch)
        response_data = {
            "message": "Branch Created Successfully",
            "data": serializer.data,
        }   
        return Response(response_data, status=status.HTTP_201_CREATED)

class GetRepoView(APIView):
    def get(self, request):
        username = request.query_params.get("username")
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        # repo_ids = UserToRepo.objects.filter(user_id=user.user_id).values_list('repo_id', flat=True)
        # print("User Repos:", repo_ids)
        repo_list = Users.objects.get(username=username).repos
        repos = Repo.objects.filter(pk__in=repo_list.all()).values()
        print(repos)
        # repo_data = [{"repo_id": repo.repo_id, "repo_name": repo.repo_name, "description": repo.description, "storage_bucket_url": repo.bucket_url} for repo in repos]
        
        response_data = {}
        for repo in repos:
            branches = Branch.objects.filter(repo_id=repo["repo_id"])
            serializer = BranchSerializer(branches, many=True)
            resp_data = {"details": repo}
            resp_data["branches"] = serializer.data
            response_data[repo["repo_name"]] = resp_data
            
        return Response(response_data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        pw = request.data.get("password")
        # TODO; include the hashing later on
        user = Users.objects.filter(username=username).values("password")
        if user[0].get("password") == pw:
            response_data = {"message": "Login Successfully"}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {"message": "Invalid credentials"}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


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

class GetObjectsView(APIView):
    def get(self, request):
        # repo_id = request.query_params.get("id")
        # branch = request.query_params.get("branch")
        # branch = Branch.objects.get(repo_id=repo_id, branch_name=branch)
        branch_id = request.query_params.get("branch_id")
        branch = Branch.objects.get(branch_id=branch_id)

        commit = branch.commit_id
        metarange = commit.meta_id
        ranges = metarange.ranges.all()
        kvs = []
        for range in ranges:
            files = range.files.all()
            serializer = FilesSerializer(files, many=True)
            kvs.append(serializer.data)

        return Response({"files": kvs}, status=status.HTTP_200_OK)


# class GetRepoView(APIView):
#     def get(self, request):
#         username = request.query_params.get("username")
#         try:
#             user = Users.objects.get(username=username)
#         except Users.DoesNotExist:
#             return Response(
#                 {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         repo_ids = UserToRepo.objects.filter(user_id=user.user_id).values_list(
#             "repo_id", flat=True
#         )
#         print("User Repos:", repo_ids)

#         repos = Repo.objects.filter(repo_id__in=repo_ids)
#         repo_data = [
#             {
#                 "repo_id": repo.repo_id,
#                 "repo_name": repo.repo_name,
#                 "description": repo.description,
#                 "storage_bucket_url": repo.bucket_url,
#             }
#             for repo in repos
#         ]

#         response_data = {}
#         for repo in repo_data:
#             branches = Branch.objects.filter(repo_id=repo["repo_id"])
#             serializer = BranchSerializer(branches, many=True)
#             resp_data = {"details": repo}
#             resp_data["branches"] = serializer.data
#             response_data[repo["repo_name"]] = resp_data

#         return Response(response_data, status=status.HTTP_200_OK)
