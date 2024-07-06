from django.db import models
import uuid


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Files(models.Model):
    url = models.URLField(primary_key=True)
    meta_data = models.TextField()

    def __str__(self):
        return self.url


class Range(models.Model):
    range_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    files = models.ManyToManyField(Files)

    def __str__(self):
        return self.range_id


class MetaRange(models.Model):
    meta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ranges = models.ManyToManyField(Range, default=[])

    def __str__(self):
        return self.meta_id, self.ranges


class Commit(models.Model):
    commit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_id = models.OneToOneField(MetaRange, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    add = models.ManyToManyField(Files, default=[], related_name="add_set")
    edit = models.ManyToManyField(
        Files, default=[], related_name="edit_set"
    )  
    remove = models.ManyToManyField(Files, default=[], related_name="remove_set")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.commit_id, self.meta_id


class Repo(models.Model):
    repo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    repo_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    default_branch = models.CharField(max_length=100)
    bucket_url = models.URLField(null=True)

    def __str__(self):
        return self.repo_id, self.repo_name


class Branch(models.Model):
    branch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_name = models.CharField(max_length=100)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    commit_id = models.ForeignKey(
        Commit, on_delete=models.CASCADE, related_name="commits"
    )
    repo_id = models.ForeignKey(
        Repo, on_delete=models.CASCADE, related_name="repo", null=False
    )

    class Meta:
        ordering = ["-created_timestamp"]

    def __str__(self):
        return self.branch_id, self.commit_id


class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    repos = models.ManyToManyField(Repo, default=[])
    email = models.EmailField()

    def __str__(self):
        return self.user_id


class UserToRepo(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user")
    repo_id = models.ForeignKey(
        Repo, on_delete=models.CASCADE, related_name="repo_user"
    )
    role = models.CharField(max_length=100, default="admin")  # what other roles

    def __str__(self):
        return self.role
