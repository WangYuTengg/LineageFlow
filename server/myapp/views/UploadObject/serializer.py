from rest_fromwork import serializers
from myapp.models import Commit
from myapp.gcs_utils import GCS

class UploadFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required = True)
    objectName = serializers.CharField(required = True)
    repo = serializers.CharField(required = True) 
    branch = serializers.CharField(required = True)
    bucket_url = serializers.URLField(required = False, allow_blank = True, default = '')
    
    class Meta: 
        model = Commit 
        field = ['repo', 'branch', 'file', 'objectName']
        
    def create(self, validated_data):
        gcs = GCS() 
        
        file = validated_data.get('file')
        object_name = validated_data.get('objectName')
        repo = validated_data.get('repo')
        branch = validated_data.get('branch')
        bucket_url = validated_data.get('bucket_url', '')
        
        if bucket_url:
            bucket_name = gcs.get_bucket_name(bucket_link=bucket_url)
            if not gcs.bucket_exists(bucket_name):
                bucket_name, bucket_url = gcs.create_bucket(bucket_name)
        
 
        public_url = gcs.upload_to_gcs(file, object_name, bucket_url)    
        metadata = gcs.get_file_metadata(bucket_url, object_name) 
        objects_metadata = gcs.list_gcs_objects_from_prefix(bucket_link = bucket_url, prefix = object_name)
        ranges = gcs.group_into_ranges(objects_metadata)