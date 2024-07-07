from django.db import models
import uuid


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# 1 File has 1 range:
# file.range -> to get the range of the file
class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.TextField()
    # gc bucket link 
    loc = models.URLField()
    meta_data = models.TextField()
    version = models.IntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    range = models.ForeignKey(
        "Range",
        related_name="files",
        on_delete=models.CASCADE,
        null=True,
    )
    class Meta:
        unique_together = ('file_name', 'version')

    def __str__(self):
        return self.file_name


#  range.metaranges.all() -> to get metaranges of a range
# 1 Range -> Many files
# range.files.all() -> to get all files associated with the range
class Range(models.Model):
    range_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.range_id)


# Many MetaRange -> Many Ranges (metarange.ranges.all() -> to get ranges of a metarange)
# 1 meta range - 1 commit (so new commits, we MUST generate a new meta range)
# To get commit of meta range, use meta_range.commit
class MetaRange(models.Model):
    meta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranges = models.ManyToManyField(Range, related_name="metaranges", default=[])
    created_timestamp = models.DateTimeField(auto_now_add=True)
    commit = models.OneToOneField(
        "Commit", related_name="meta_range", on_delete=models.CASCADE, null=True
    )

    
    def __str__(self):
        return str(self.meta_id)


# 1 Branch -> Many Commits (For commit history, sort by TimeStamp)
# branch.commits.all() -> Returns all commits associated with the branch
# to get meta range of commit, use commit.meta_range (related_name in MetaRange)
class Commit(models.Model):
    commit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commit_message = models.TextField(null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    add = models.ManyToManyField(File, default=[], related_name="add_set")
    edit = models.ManyToManyField(File, default=[], related_name="edit_set")
    remove = models.ManyToManyField(File, default=[], related_name="remove_set")
    branch = models.ForeignKey(
        "Branch", related_name="commits", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_timestamp"]

    def __str__(self):
        return str(self.commit_id)


# 1 Repo -> Many Branches
# repo.branches.all() -> give us all the branches related to the repo
class Branch(models.Model):
    branch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_name = models.CharField(max_length=100)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    repo = models.ForeignKey(
        "Repo", on_delete=models.CASCADE, related_name="branches", null=False
    )

    class Meta:
        ordering = ["-created_timestamp"]

    def __str__(self):
        return str(self.branch_id)


# user.repo_set.all() -> Returns all repos associated with the user
# repo.users_set.all() -> Returns all users associated with the repo
class Repo(models.Model):
    repo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    repo_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    default_branch = models.CharField(max_length=100)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    bucket_url = models.URLField(null=True)

    def __str__(self):
        return str(self.repo_id)


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    repos = models.ManyToManyField(Repo, default=[])  # many user <-> many repo
    email = models.EmailField()

    def __str__(self):
        return str(self.user_id)
