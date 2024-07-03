from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Item, Files, Range, MetaRange, Commit, Branch, Repo, Users
from django.db import transaction, IntegrityError


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ["name", "description"]

#     def create(self, validated_data):
#         return Item.objects.create(**validated_data)


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ["url", "meta_data"]

    def create(self, validated_data):
        return Files.objects.create(**validated_data)


class RangeSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=Files.objects.all(), many=True)

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
    meta_id = serializers.PrimaryKeyRelatedField(queryset=MetaRange.objects.all())

    class Meta:
        model = Commit
        fields = ["commit_id", "meta_id", "timestamp"]

    def create(self, validated_data):
        commit_instance = Commit.objects.create(**validated_data)
        return commit_instance


class BranchSerializer(serializers.ModelSerializer):
    commit_id = serializers.PrimaryKeyRelatedField(queryset=Commit.objects.all())

    class Meta:
        model = Branch
        fields = ["branch_name", "created_timestamp", "updated_timestamp", "commit_id"]

    def create(self, validated_data):
        branch_instance = Branch.objects.create(**validated_data)
        return branch_instance

    def update(self, instance, validated_data):
        commit_data = validated_data.pop("commit_id")
        commit_instance, created = Commit.objects.get_or_create(**commit_data)
        instance.commit_id = commit_instance
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
            branch_name = validated_data.pop("default_branch")
            with transaction.atomic():
                meta_range = MetaRange.objects.create()
                commit = Commit.objects.create(meta_id=meta_range)
                branch = Branch.objects.create(
                    branch_name=branch_name, commit_id=commit
                )
                repo = Repo.objects.create(default_branch=branch, **validated_data)

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


