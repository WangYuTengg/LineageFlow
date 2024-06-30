from rest_framework import serializers
from .models import Item


class RepositorySerializer(serializers.Serializer):
    repositoryName = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300, allow_blank=True)
    storageNamespace = serializers.CharField(max_length=100)
    defaultBranch = serializers.CharField(default="main")

    def create(self, validated_data):
        # TODO: Here you would typically create a database record
        # return Repository.objects.create(**validated_data)
        return
