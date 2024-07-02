from google.cloud import storage
import json
import re
import requests
class GCS:
    def __init__(self):
        self.client = storage.Client()

    def get_bucket_name(self, bucket_link):
        # Extract bucket name from URL
        match = re.match(r"https://storage.googleapis.com/([^/]+)/?", bucket_link)
        if match:
            return match.group(1)
        raise ValueError("Invalid bucket URL")

    def list_gcs_objects(self, bucket_link):
        bucket_name = self.get_bucket_name(bucket_link)
        bucket = self.client.bucket(bucket_name)

        blobs = bucket.list_blobs()
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
            url, metadata = next(iter(metadata_dict.items()))

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
