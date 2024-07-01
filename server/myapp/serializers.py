from rest_framework import serializers
from .models import Item, Files, Range, MetaRange, Commit, Branch


class RepositorySerializer(serializers.Serializer):
    repositoryName = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300, allow_blank=True)
    storageNamespace = serializers.CharField(max_length=100, allow_blank = True)
    defaultBranch = serializers.CharField(default="main")

    def create(self, validated_data):
        # TODO: Here you would typically create a database record
        # return Repository.objects.create(**validated_data)
        return

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description']
    
    def create(self, validated_data):
        return Item.objects.create(**validated_data)
    
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['url', 'meta_data']
    
    def create(self, validated_data):
        return Files.objects.create(**validated_data)


class RangeSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(queryset=Files.objects.all(), many=True)

    class Meta:
        model = Range
        fields = ['range_id', 'files']

    def create(self, validated_data):
        files_data = validated_data.pop('files')
        range_instance = Range.objects.create(**validated_data)
        range_instance.files.set(files_data)
        return range_instance

    def update(self, instance, validated_data):
        files_data = validated_data.pop('files')
        instance.range_id = validated_data.get('range_id', instance.range_id)
        instance.save()
        instance.files.set(files_data)
        return instance


class MetaRangeSerializer(serializers.ModelSerializer):
    ranges = serializers.PrimaryKeyRelatedField(queryset=Range.objects.all(), many=True)

    class Meta:
        model = MetaRange
        fields = ['meta_id', 'ranges']

    def create(self, validated_data):
        ranges_data = validated_data.pop('ranges')
        meta_range_instance = MetaRange.objects.create(**validated_data)
        meta_range_instance.ranges.set(ranges_data)
        return meta_range_instance

    def update(self, instance, validated_data):
        ranges_data = validated_data.pop('ranges')
        instance.meta_id = validated_data.get('meta_id', instance.meta_id)
        instance.save()
        instance.ranges.set(ranges_data)
        return instance


class CommitSerializer(serializers.ModelSerializer):
    meta_id = serializers.PrimaryKeyRelatedField(queryset=MetaRange.objects.all())

    class Meta:
        model = Commit
        fields = ['commit_id', 'meta_id', 'timestamp']

    def create(self, validated_data):
        commit_instance = Commit.objects.create(**validated_data)
        return commit_instance

    def update(self, instance, validated_data):
        meta_data = validated_data.pop('meta_id')
        meta_instance, created = MetaRange.objects.get_or_create(**meta_data)
        instance.meta_id = meta_instance
        instance.commit_id = validated_data.get('commit_id', instance.commit_id)
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    commit_id = serializers.PrimaryKeyRelatedField(queryset=Commit.objects.all())

    class Meta:
        model = Branch
        fields = ['branch_name', 'created_timestamp', 'updated_timestamp', 'commit_id']

    def create(self, validated_data):
        branch_instance = Branch.objects.create(**validated_data)
        return branch_instance

    def update(self, instance, validated_data):
        commit_data = validated_data.pop('commit_id')
        commit_instance, created = Commit.objects.get_or_create(**commit_data)
        instance.commit_id = commit_instance
        instance.branch_name = validated_data.get('branch_name', instance.branch_name)
        instance.save()
        return instance