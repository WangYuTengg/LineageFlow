from rest_framework import serializers
import logging
from myapp.models import Repo, MetaRange, Commit, Branch, Range, Files, Users, UserToRepo
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from ...gcs_utils import GCS

logger = logging.getLogger(__name__)


class CreateRepositorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True, write_only = True)
    default_branch = serializers.CharField(write_only=True)
    bucket_url = serializers.URLField(required=False, allow_blank=True, default="")
    repo_name = serializers.CharField(write_only=True)
    description = serializers.CharField(write_only=False, allow_blank=True, default="")
    storage_bucket_name = serializers.CharField(required=True, write_only = True)

    class Meta:
        model = Repo
        fields = ["repo_name", "description", "default_branch", "bucket_url", "username", "storage_bucket_name"]

    def create(self, validated_data):
        try:
            branch_name = validated_data.pop("default_branch")
            bucket_url = validated_data.pop("bucket_url", "")
            username = validated_data.pop("username")
            storage_bucket_name = validated_data.pop('storage_bucket_name')
            
            objects = None
            ranges = None
            gcs = GCS()
            storage_bucket_link = gcs.create_bucket(bucket_name=storage_bucket_name)
            
            if bucket_url:
                objects = gcs.list_gcs_objects_from_prefix(bucket_url)
                ranges = gcs.group_into_ranges(objects)

            with transaction.atomic():
                files_list = []
                ranges_list = []

                if objects:
                    for obj in objects:
                        key, value = next(iter(obj.items()))
                        file = Files.objects.create(url=key, meta_data=value)
                        files_list.append(file)
                if ranges:
                    for rng in ranges:
                        range_obj = Range.objects.create()
                        range_obj.files.set(rng)
                        ranges_list.append(range_obj)

                meta_range = MetaRange.objects.create()
                meta_range.ranges.set(ranges_list)
                
                user = Users.objects.get(username = username)

                commit = Commit.objects.create(meta_id=meta_range)
                repo = Repo.objects.create(**validated_data, bucket_url = storage_bucket_link)
                
                userToRepo = UserToRepo.objects.create(user_id = user, repo_id = repo)
                
                branch = Branch.objects.create(
                    branch_name=branch_name, commit_id=commit, repo_id=repo
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
