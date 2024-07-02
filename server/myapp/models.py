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
    ranges = models.ManyToManyField(Range)

    def __str__(self):
        return self.meta_id


class Commit(models.Model):
    commit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_id = models.OneToOneField(MetaRange, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.commit_id


class Branch(models.Model):
    branch_name = models.CharField(max_length=100, primary_key=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    commit_id = models.ForeignKey(
        Commit, on_delete=models.CASCADE, related_name="commits"
    )

    class Meta:
        ordering = ["-created_timestamp"]

    def __str__(self):
        return self.branch_name


class Repo(models.Model):
    repo_name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(default="")
    default_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="branch"
    )
    gc_bucket = models.URLField(default="")

    def __str__(self):
        return self.repo_name
