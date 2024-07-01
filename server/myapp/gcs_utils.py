from google.cloud import storage
import json 
import math

class GCS: 
    def __init__(self):
        self.client = storage.Client() 

    def list_gcs_objects(self, bucket_name):
        bucket = self.client.get_bucket(bucket_name)
        
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
            objects_metadata.append(metadata)
            
        objects_metadata.sort(key = lambda x: x["name"])
        
        return objects_metadata
    
    def group_into_ranges(self, objects_metadata, max_size=2 * 1024 * 1024): 
        ranges = [] 
        current_range = {} 
        current_size = 0 
        
        for metadata in objects_metadata:
            metadata_str = json.dumps(metadata)
            metadata_size = len(metadata_str.encode('utf-8')) 
            
            if current_size + metadata_size > max_size: 
                ranges.append(current_range)
                current_range = {}
                current_size = 0 
                
            current_range[metadata["name"]] = metadata
            current_size += metadata_size 
            
        if current_range: 
            ranges.append(current_range)
            
        return ranges

# if __name__ == "__main__":
#     bucket_name = "techjam"
#     gcs = GCS()
#     objects_metadata = gcs.list_gcs_objects(bucket_name)
#     ranges = gcs.group_into_ranges(objects_metadata)  # Correcting the method call

#     for i, range_group in enumerate(ranges):
#         print(f"Range {i + 1}:")
#         for object_pointer, metadata in range_group.items():
#             print(f"  {object_pointer}: {metadata}")
#         print()