from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from myapp.models import Branch, Repo, Range, Commit, MetaRange, File
from myapp.gcs_utils import GCS
from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.exceptions import ValidationError
import json
import logging
from urllib.parse import quote, urlparse
import re

class Test(APIView):
    def post(self, request):
        print('POST request received')
        # Extracting required data from the request
        repo_name = request.data.get('repo')
        branch_name = request.data.get('branch')
        files = request.FILES.getlist('files')
        relative_paths = request.data.getlist('relative_paths')
        storage_bucket_url = request.data.get('storage_bucket')
        storage_bucket_name = urlparse(storage_bucket_url).path.split('/')[1]
        
        print(f'Repo: {repo_name}, Branch: {branch_name}, Files: {len(files)}, Relative Paths: {len(relative_paths)}, Storage Bucket URL: {storage_bucket_url}')
        
        repo = self.get_repo(repo_name)
        branch = self.get_branch(repo, branch_name)
        
        latest_commit = Commit.objects.filter(branch=branch).order_by('-created_timestamp').first()
        print(latest_commit)
        
        gcs = GCS()
        
        if not latest_commit:
            # Handle case with no existing commits
            print('Handling empty branch')
            self.handle_empty_branch(files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs, branch)
        else:
            print('Handling NOT empty branch')
            # Handle case with existing commits
            self.handle_existing_branch(files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs, branch, latest_commit)
        
        return Response({"message": "Success"})
    
    def get_repo(self, repo_name):
        try:
            repo = Repo.objects.get(repo_name=repo_name)
            print(f'Found repo: {repo_name}')
            return repo
        except Repo.DoesNotExist:
            print(f'Repository "{repo_name}" not found')
            raise ValidationError(f"Repository '{repo_name}' not found")
    
    def get_branch(self, repo, branch_name):
        try:
            branch = Branch.objects.get(repo=repo, branch_name=branch_name)
            print(f'Found branch: {branch_name} in repo: {repo.repo_name}')
            return branch
        except Branch.DoesNotExist:
            print(f'Branch "{branch_name}" not found in repository "{repo.repo_name}"')
            raise ValidationError(f"Branch '{branch_name}' not found in repository '{repo.repo_name}'")
    
    def partition_files_by_size(self, file_objs, max_partition_size=2 * 1024 * 1024):
        print('Partitioning files by size')
        partitions = []
        current_partition = []
        current_partition_size = 0
        
        for file_obj in file_objs:
            print(file_obj)
            print(file_obj.meta_data)
            meta_data = json.loads(file_obj.meta_data)
            file_size = meta_data["size"]  # Assuming size is stored as a int
            print(f'File: {file_obj.file_name}, Size: {file_size}')
            
            if current_partition_size + file_size <= max_partition_size:
                current_partition.append(file_obj)
                current_partition_size += file_size
            else:
                partitions.append(current_partition)
                current_partition = [file_obj]
                current_partition_size = file_size

        if current_partition:
            partitions.append(current_partition)

        print(f'Created {len(partitions)} partitions')
        return partitions
    
    def handle_empty_branch(self, files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs, branch):
        print('Handling empty branch: creating file objects and partitions')
        with transaction.atomic():
            list_of_file_obj = self.create_file_objects(files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs)
            partitions = self.partition_files_by_size(list_of_file_obj)
            list_of_range_objects = self.create_ranges_and_partitions(partitions)
            self.create_metarange_and_commit(branch, list_of_range_objects, list_of_file_obj_add=list_of_file_obj)
    
    def handle_existing_branch(self, files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs, branch, latest_commit):
        print('Handling existing branch')
        existing_ranges = {}
        all_existing_ranges = list(latest_commit.meta_range.ranges.all())
        files_edited = []
        files_first_time_added = []

        for file, relative_path in zip(files, relative_paths):
            file_name = f"{repo_name}/{branch_name}/{relative_path}"
            print(f'Processing file: {file_name}')
            existing_file = File.objects.filter(file_name=file_name).order_by('-version').first()

            if not existing_file:
                # Upload and create file for the first time
                print(f'Uploading and creating new file: {file_name}')
                new_file_obj = self.upload_and_create_file(file, relative_path, repo_name, branch_name, storage_bucket_url, gcs)
                files_first_time_added.append(new_file_obj)
            else:
                # if the file exists
                # Handle existing file by creating a new version
                print(f'Existing file found: {file_name}, creating new version')
                # get range of existing file
                existing_range_obj = existing_file.range
                
                # From the list of ranges that this meta range contains remove this range that belongs to the existing file
                print("all_existing_ranges before", all_existing_ranges)
                if existing_range_obj in all_existing_ranges:
                    all_existing_ranges.remove(existing_range_obj)
                    print("all_existing_ranges after", all_existing_ranges)

                # append this range to a dictionary that stores the repeating files and the range it belongs to
                existing_ranges.setdefault(existing_range_obj, []).append(existing_file)
                print("existing ranges", existing_ranges)
                
                # push the edited file to gcs
                new_file_obj = self.upload_and_create_file(file, relative_path, repo_name, branch_name, storage_bucket_url, gcs, existing_file.version + 1)
                files_edited.append(new_file_obj)
                print("files edited: ", files_edited)
        
        print("files edited after loop: ", files_edited)
        print("existing ranges after", existing_ranges)
        all_remaining_files = []
        for rjo, outer in existing_ranges.items():
            print(rjo, outer)
            remaining_files = list(rjo.files.exclude(id__in=[f.id for f in outer]))
            print("remaining files", remaining_files)
            all_remaining_files.extend(remaining_files)
            all_remaining_files.extend(files_edited)
        
        print("all remaining files after", all_remaining_files)
        # Partition remaining files and create ranges
        print(f'Partitioning remaining files: {len(all_remaining_files)}')
        partitions = self.partition_files_by_size(all_remaining_files)
        list_of_range_objects = self.create_ranges_and_partitions(partitions)
        all_existing_ranges.extend(list_of_range_objects)
        print('Creating metarange and commit')
        self.create_metarange_and_commit(branch, all_existing_ranges, list_of_file_obj_add=files_first_time_added, list_of_file_edit=files_edited)
    
    def upload_and_create_file(self, file, relative_path, repo_name, branch_name, storage_bucket_url, gcs, version=1):
        # Upload file to GCS and create the File object
        print(f'Uploading file: {relative_path} with version: {version}')
        file_name = f"{repo_name}/{branch_name}/{relative_path}"
        obj_data = gcs.upload_and_get_metadata(file, relative_path, storage_bucket_url, version)
        print(obj_data)
        loc = obj_data['url']
        meta_data = obj_data['meta_data']
        new_file = File.objects.create(
            file_name=file_name,
            loc=loc,
            meta_data=meta_data,
            version=version
        )
        print(f'Created file object: {file_name}, Version: {version}')
        return new_file

    def create_file_objects(self, files, relative_paths, repo_name, branch_name, storage_bucket_url, gcs):
        print('Creating file objects')
        list_of_file_obj = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.upload_and_create_file, file, relative_path, repo_name, branch_name, storage_bucket_url, gcs) for file, relative_path in zip(files, relative_paths)]
            for future in as_completed(futures):
                list_of_file_obj.append(future.result())
        
        list_of_file_obj.sort(key=lambda x: x.file_name)
        print(f'Created {len(list_of_file_obj)} file objects')
        return list_of_file_obj
    
    def create_ranges_and_partitions(self, partitions):
        print('Creating ranges and partitions')
        list_of_range_objects = []
        for partition in partitions:
            partition_size = sum(int(json.loads(file.meta_data)['size']) for file in partition)  # Calculate total partition size
            range_obj = Range.objects.create(size=partition_size)  # Create Range with partition size
            range_obj.files.add(*partition)
            list_of_range_objects.append(range_obj)
        print(f'Created {len(list_of_range_objects)} range objects')
        return list_of_range_objects

    def create_metarange_and_commit(self, branch, list_of_range_objects, list_of_file_obj_add=[], list_of_file_edit=[]):
        print('Creating MetaRange and Commit')
        new_metarange = MetaRange.objects.create()
        new_metarange.ranges.add(*list_of_range_objects)

        # Create the commit without linking the meta_range initially
        new_commit = Commit.objects.create(
            branch=branch,
            commit_message="Auto-generated commit"  # Add a default message or adjust as necessary
        )

        # Link the meta_range to the commit
        new_metarange.commit = new_commit
        new_metarange.save()

        # Add files to the commit
        new_commit.add.add(*list_of_file_obj_add)
        new_commit.edit.add(*list_of_file_edit)
        
        print('MetaRange and Commit created successfully')
        return new_commit  # Optionally return the new commit or metarange if needed

