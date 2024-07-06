from google.cloud import storage
import json
import re
import requests
import os
from rest_framework.exceptions import ValidationError
from google.api_core.exceptions import GoogleAPICallError
import urllib.parse


class GCS:
    def __init__(self):
        self.client = storage.Client()
        
    def upload_to_gcs(self, file, object_name, bucket_link):
        bucket_name = self.get_bucket_name(bucket_link)
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_file(file, content_type=file.content_type)
        public_url = blob.public_url
        return self.ensure_consistent_url(public_url)

    def ensure_consistent_url(self, url):
        decoded_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlsplit(decoded_url)
        encoded_path = urllib.parse.quote(parsed_url.path)
        return urllib.parse.urlunsplit((
            parsed_url.scheme,
            parsed_url.netloc,
            encoded_path,
            parsed_url.query,
            parsed_url.fragment
        ))

    
    def get_bucket_name(self, bucket_link):
        # Extract bucket name from URL
        match = re.match(r"https://storage.googleapis.com/([^/]+)/?", bucket_link)
        if match:
            return match.group(1)
        raise ValueError("Invalid bucket URL")
    
    def pull_data(self, url):
        response = requests.get(url)
        if response.status_code == 200: 
            return response.content 
        else:
            response.raise_for_status()
            
    def delete_file(self, bucket_name, file_url):
        bucket = self.client.bucket(bucket_name)
        blob_name = file_url.split('/')[-1]
        blob = bucket.blob(blob_name)
        blob.delete()
    
    def get_file_metadata(self, bucket_link, object_name):
        bucket_name = self.get_bucket_name(bucket_link)
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        
        # Ensure the blob exists and has metadata
        blob.reload()
        if blob.updated is None:
            return {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "updated": None,
                "generation": blob.generation,
                "metageneration": blob.metageneration
            }

        metadata = {
            "name": blob.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "updated": blob.updated.isoformat(),
            "generation": blob.generation,
            "metageneration": blob.metageneration
        }

        return metadata
    
    def upload_and_get_metadata(self, file, relative_path, storage_bucket, version=1):
        relative_path_with_version = f"{relative_path}?v={version}"
        public_url = self.upload_to_gcs(file, relative_path_with_version, storage_bucket)
        metadata = self.get_file_metadata(storage_bucket, relative_path_with_version)
        metadata_json = json.dumps(metadata)
        return {"url": public_url, "meta_data": metadata_json}

    def create_bucket(self, bucket_name):
        # Convert the bucket name to lowercase and replace invalid characters
        bucket_name = bucket_name.lower().replace('_', '-')
        
        # Remove any characters that are not allowed
        bucket_name = re.sub(r'[^a-z0-9-.]', '', bucket_name)

        # Ensure the bucket name is within the allowed length
        bucket_name = bucket_name[:63]

        # Ensure the bucket name starts and ends with a letter or number
        if not re.match(r'^[a-z0-9]', bucket_name):
            bucket_name = 'a' + bucket_name
        if not re.match(r'[a-z0-9]$', bucket_name):
            bucket_name = bucket_name + 'a'
        
        # Ensure the bucket name is at least 3 characters long
        if len(bucket_name) < 3:
            bucket_name += 'a' * (3 - len(bucket_name))

        try:
            new_bucket = self.client.create_bucket(bucket_name)
            
            # Make the bucket public
            policy = new_bucket.get_iam_policy()
            policy.bindings.append({
                'role': 'roles/storage.objectViewer',
                'members': {'allUsers'}
            })
            new_bucket.set_iam_policy(policy)
            return f"https://storage.googleapis.com/{new_bucket.name}/"
        
        except GoogleAPICallError as e:
            raise ValidationError({"google_api_error": f"A Google API error occurred: {str(e)}"})
        except Exception as e:
            raise ValidationError({"unexpected_error": f"An unexpected error occurred: {str(e)}"})

    def list_gcs_objects_from_prefix(self, bucket_link, prefix=None):
        bucket_name = self.get_bucket_name(bucket_link)
        bucket = self.client.bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=prefix)
        objects_metadata = []

        for blob in blobs:
            metadata = {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "updated": blob.updated.isoformat(),
                "generation": blob.generation,
                "metageneration": blob.metageneration
            }
            
            data_object_pointer = {
                f"{bucket_link}{blob.name}" : metadata
            }
            objects_metadata.append(data_object_pointer)

        objects_metadata.sort(key=lambda x: list(x.keys())[0])

        return objects_metadata

    def group_into_ranges(self, objects_metadata, max_size=2 * 1024 * 1024):
        ranges = []
        current_range = {}
        current_size = 0

        for metadata_dict in objects_metadata:
            # Extract the key (URL) and metadata
            url = metadata_dict['url']
            metadata = metadata_dict['meta_data']

            try:
                metadata_str = json.dumps(metadata)
                metadata_size = len(metadata_str.encode('utf-8'))
            except (TypeError, ValueError) as e:
                print(f"Error serializing metadata: {metadata} -> {e}")
                continue

                if current_size + metadata_size > max_size:
                    ranges.append(current_range)
                    current_range = {}
                    current_size = 0

            current_range[url] = metadata
            current_size += metadata_size

        if current_range:
            ranges.append(current_range)

        return ranges

def send_metadata_to_api(bucket_url, metadata):
    url = "http://your-api-endpoint.com/your-endpoint"
    data = {
        "url": bucket_url,
        "meta_data": metadata
    }
    response = requests.post(url, json=data)
    return response.json()

# if __name__ == "__main__":
#     bucket_link = "https://storage.googleapis.com/techjam/"
#     gcs = GCS()
#     objects_metadata = gcs.list_gcs_objects(bucket_link)
#     ranges = gcs.group_into_ranges(objects_metadata)

#     for i, range_group in enumerate(ranges):
#         print(f"Range {i + 1}:")
#         for object_pointer, metadata in range_group.items():
#             print(f"  {object_pointer}: {metadata}")
#             response = send_metadata_to_api(bucket_link, metadata)
#             print(response)
#         print()
