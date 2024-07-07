from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    File,
    Range,
    MetaRange,
    Commit,
    Branch,
    Repo,
    Users,
)
from django.db import transaction, IntegrityError


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file_name",
            "loc",
            "meta_data",
            "version",
            "range",
        ]  # include other necessary fields

    def create(self, validated_data):
        return File.objects.create(**validated_data)


class RangeSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), many=True)

    class Meta:
        model = Range
        fields = ["range_id", "files"]

    def create(self, validated_data):
        files_data = validated_data.pop("files")
        range_instance = Range.objects.create(**validated_data)
        range_instance.files.set(files_data)
        return range_instance


class MetaRangeSerializer(serializers.ModelSerializer):
    ranges = serializers.PrimaryKeyRelatedField(queryset=Range.objects.all(), many=True)

    class Meta:
        model = MetaRange
        fields = ["meta_id", "ranges"]

    def create(self, validated_data):
        ranges_data = validated_data.pop("ranges")
        meta_range_instance = MetaRange.objects.create(**validated_data)
        meta_range_instance.ranges.set(ranges_data)
        return meta_range_instance


class CommitSerializer(serializers.ModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Commit
        fields = ["commit_id", "commit_message", "created_timestamp", "branch_id"]

    def create(self, validated_data):
        commit_instance = Commit.objects.create(**validated_data)
        return commit_instance


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "branch_id",
            "branch_name",
            "created_timestamp",
            "updated_timestamp",
            "repo_id",
        ]

    def create(self, validated_data):
        branch_instance = Branch.objects.create(**validated_data)
        return branch_instance

    def update(self, instance, validated_data):
        instance.branch_name = validated_data.get("branch_name", instance.branch_name)
        instance.save()
        return instance


class RepositorySerializer(serializers.ModelSerializer):
    default_branch = serializers.CharField(write_only=True)

    class Meta:
        model = Repo
        fields = ["repo_name", "description", "default_branch", "bucket_url"]

    def create(self, validated_data):
        try:
            branch_name = validated_data.get("default_branch")
            with transaction.atomic():
                meta_range = MetaRange.objects.create()
                commit = Commit.objects.create(meta_id=meta_range)
                repo = Repo.objects.create(**validated_data)
                branch = Branch.objects.create(
                    branch_name=branch_name, commit_id=commit, repo_id=repo
                )

            return repo

        except IntegrityError as e:
            print(f"An integrity error occurred: {str(e)}")
            raise ValidationError(
                {"database_error": "A database integrity error occurred."}
            )

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise ValidationError(
                {"unexpected_error": f"An unexpected error occurred: {str(e)}"}
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "password", "email", "repos"]

    def create(self, validated_data):
        try:
            name = validated_data.pop("username")
            pw = validated_data.pop("password")
            email = validated_data.pop("email")

            user_acc = Users.objects.create(username=name, password=pw, email=email)
            return user_acc

        except IntegrityError as e:
            print(f"An integrity error occurred: {str(e)}")
            raise ValidationError(
                {"database_error": "A database integrity error occurred."}
            )

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise ValidationError(
                {"unexpected_error": f"An unexpected error occurred: {str(e)}"}
            )
