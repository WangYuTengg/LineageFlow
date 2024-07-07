from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Branch, Repo, Range, Commit, MetaRange, File
from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ValidationError


class DeleteFile(APIView):
    """
    file = {
        "file_name":
        "id":
        "loc":
        "metadata" :
        "range":
    }
    """

    def post(self, request):
        files = request.data.get("files_list")
        repo_name = request.data.get("repo")
        branch_name = request.data.get("branch")
        commit_message = request.data.get("commit_message")

        repo = self.get_repo(repo_name)
        branch = self.get_branch(repo, branch_name)

        latest_commit = (
            Commit.objects.filter(branch=branch).order_by("-created_timestamp").first()
        )

        files_to_delete = []
        list_of_file_obj_delete = []
        current_ranges = []

        for file in files:
            target_range = self.get_range(range_id=file["range"])
            if target_range not in current_ranges:
                current_ranges.append(target_range)
            files_to_delete.append(file["file_name"])
            list_of_file_obj_delete.append(file)

        try:
            self.create_metarange_and_commit(
                branch,
                current_ranges,
                files_to_delete,
                list_of_file_obj_delete,
                commit_message,
            )
            return Response(
                {"message": "Files deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except (IntegrityError, DatabaseError) as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_range(self, range_id):
        try:
            range_obj = Range.objects.get(range_id=range_id)
            print(f"Found range: {range_id}")
            return range_obj
        except Range.DoesNotExist:
            print(f"Range {range_id} not found")
            raise ValidationError(f"Range {range_id} not found")

    def get_repo(self, repo_name):
        try:
            repo = Repo.objects.get(repo_name=repo_name)
            print(f"Found repo: {repo_name}")
            return repo
        except Repo.DoesNotExist:
            print(f'Repository "{repo_name}" not found')
            raise ValidationError(f"Repository '{repo_name}' not found")

    def get_branch(self, repo, branch_name):
        try:
            branch = Branch.objects.get(repo=repo, branch_name=branch_name)
            print(f"Found branch: {branch_name} in repo: {repo.repo_name}")
            return branch
        except Branch.DoesNotExist:
            print(f'Branch "{branch_name}" not found in repository "{repo.repo_name}"')
            raise ValidationError(
                f"Branch '{branch_name}' not found in repository '{repo.repo_name}'"
            )

    def get_file(self, file_id):
        try:
            file_obj = File.objects.get(id=file_id)
            print(f"Found file: {file_id}")
            return file_obj
        except File.DoesNotExist:
            print(f"File {file_id} not found")
            raise ValidationError(f"File {file_id} not found")

    def create_metarange_and_commit(
        self,
        branch,
        current_ranges,
        list_of_file_name_delete=[],
        list_of_file_obj_delete=[],
        commit_message="Auto-generated commit",
    ):
        with transaction.atomic():
            try:
                print("Creating new range with undeleted files")
                newly_created_ranges = []
                for range_obj in current_ranges:
                    files_in_this_range = range_obj.files.all()
                    print(f"files in range: {files_in_this_range}")

                    new_range = Range.objects.create()
                    for file_name in files_in_this_range:
                        file_obj = (
                            File.objects.get_queryset()
                            .filter(file_name=file_name)
                            .last()
                        )
                        if file_obj.file_name in list_of_file_name_delete:
                            continue

                        file = File.objects.create(
                            file_name=file_obj.file_name,
                            loc=file_obj.loc,
                            meta_data=file_obj.meta_data,
                            version=file_obj.version + 1,
                            range=new_range,
                        )
                        file.save()
                        new_range.files.add(file)

                    new_range.save()

                    print(f"new files in range: {new_range.files.all()}")
                    newly_created_ranges.append(new_range)

                print("Newly created ranges:", newly_created_ranges)

                print("Creating MetaRange and Commit")
                new_metarange = MetaRange.objects.create()
                new_metarange.ranges.add(*newly_created_ranges)

                # Create the commit without linking the meta_range initially
                new_commit = Commit.objects.create(
                    branch=branch,
                    commit_message=commit_message,
                )
                print("Commit created successfully")

                # Link the meta_range to the commit
                new_metarange.commit = new_commit

                for file_obj in list_of_file_obj_delete:
                    new_commit.remove.add(self.get_file(file_obj["id"]))
                print("Files deleted added to commit_remove successfully")

                new_metarange.save()
                new_commit.save()
                print("Metarange & commit saved successfully")
            except Exception as e:
                print(f"Error: {str(e)}")
                raise e
