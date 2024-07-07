from rest_framework import serializers
import logging
from myapp.models import Repo, MetaRange, Commit, Branch, Range, File, Users
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from ...gcs_utils import GCS

logger = logging.getLogger(__name__)

class CreateRepositorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    default_branch = serializers.CharField(write_only=True)
    bucket_url = serializers.URLField(required=False, allow_blank=True, default="")
    repo_name = serializers.CharField(write_only=True)
    description = serializers.CharField(write_only=False, allow_blank=True, default="")
    storage_bucket_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Repo
        fields = [
            "repo_name",
            "description",
            "default_branch",
            "bucket_url",
            "username",
            "storage_bucket_name",
        ]

    def create(self, validated_data):
        try:
            branch_name = validated_data.get("default_branch")
            bucket_url = validated_data.get("bucket_url", "")
            username = validated_data.pop("username")
            storage_bucket_name = validated_data.get("storage_bucket_name")
            repo_name = validated_data.get("repo_name")

            gcs = GCS()
            storage_bucket_link = gcs.create_bucket(bucket_name=storage_bucket_name)

            objects = None
            if bucket_url:
                objects = gcs.list_gcs_objects_from_prefix(bucket_url)

            with transaction.atomic():
                files_list = []
                user = Users.objects.get(username=username)
                validated_data.pop("bucket_url", None)
                validated_data.pop("storage_bucket_name", None)

                # Create repository and associate with user
                repo = Repo.objects.create(
                    **validated_data, bucket_url=storage_bucket_link
                )
                user.repos.add(repo)

                # Create default branch
                branch = Branch.objects.create(branch_name=branch_name, repo=repo)

                if objects:
                    for obj in objects:
                        loc = obj['loc']
                        metadata = obj['metadata']
                        file_name = f"{repo_name}/{branch_name}/{metadata['name']}"
                        size = metadata['size']
                        file = File.objects.create(
                            file_name=file_name, 
                            loc=loc, 
                            meta_data=metadata,
                            version=1
                        )
                        files_list.append(file)
                    
                    partitions = self.partition_files_by_size(files_list)
                    ranges = self.create_ranges_and_partitions(partitions)
                    self.create_metarange_and_commit(
                        branch=branch,
                        list_of_range_objects=ranges,
                        list_of_file_obj_add=files_list,
                        commit_message="Initial commit",
                    )
          
                logger.info(
                    "Repository created successfully with repo_name: %s", repo.repo_name
                )

            return repo

        except IntegrityError as e:
            logger.error("Integrity error occurred: %s", str(e))
            raise ValidationError(
                {"database_error": "A database integrity error occurred."}
            )
        except Exception as e:
            logger.error("Unexpected error occurred: %s", str(e))
            raise ValidationError(
                {"unexpected_error": f"An unexpected error occurred: {str(e)}"}
            )

    def create_metarange_and_commit(self, branch, list_of_range_objects, list_of_file_obj_add=[], list_of_file_edit=[], commit_message="Auto-generated message"):
        print("Creating MetaRange and Commit")
        new_metarange = MetaRange.objects.create()
        new_metarange.ranges.add(*list_of_range_objects)

        # Create the commit without linking the meta_range initially
        new_commit = Commit.objects.create(
            branch=branch,
            commit_message=commit_message,
        )

        # Link the meta_range to the commit
        new_metarange.commit = new_commit
        new_metarange.save()

        # Add files to the commit
        new_commit.add.add(*list_of_file_obj_add)
        new_commit.edit.add(*list_of_file_edit)

        print("MetaRange and Commit created successfully")
        return new_commit

    def create_ranges_and_partitions(self, partitions):
        print("Creating ranges and partitions")
        list_of_range_objects = []
        for partition in partitions:
            partition_size = sum(file.meta_data["size"] for file in partition)
            range_obj = Range.objects.create(size=partition_size)
            range_obj.files.add(*partition)
            list_of_range_objects.append(range_obj)
        print(f"Created {len(list_of_range_objects)} range objects")
        return list_of_range_objects

    def partition_files_by_size(self, file_objs, max_partition_size=2 * 1024 * 1024):
        print("Partitioning files by size")
        partitions = []
        current_partition = []
        current_partition_size = 0

        for file_obj in file_objs:
            file_size = file_obj.meta_data["size"]

            if current_partition_size + file_size <= max_partition_size:
                current_partition.append(file_obj)
                current_partition_size += file_size
            else:
                partitions.append(current_partition)
                current_partition = [file_obj]
                current_partition_size = file_size

        if current_partition:
            partitions.append(current_partition)

        print(f"Created {len(partitions)} partitions")
        return partitions
