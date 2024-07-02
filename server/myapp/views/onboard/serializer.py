from rest_framework import serializers
class BucketRequestSerializer(serializers.Serializer):
    bucket_url = serializers.URLField()