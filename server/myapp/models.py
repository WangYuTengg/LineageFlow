from django.db import models


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
    range_id = models.CharField(max_length=10, primary_key=True)
    files = models.ManyToManyField(Files)
    
    def __str__(self):
        return self.range_id

class MetaRange(models.Model):
    meta_id = models.CharField(max_length=10, primary_key=True)
    ranges = models.ManyToManyField(Range)
    
    def __str__(self):
        return self.meta_id

class Commit(models.Model):
    commit_id = models.CharField(max_length=10, primary_key=True)
    meta_id = models.OneToOneField(MetaRange, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.commit_id
    
class Branch(models.Model):
    branch_name = models.CharField(max_length=100, primary_key=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    commit_id = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='commits')

    class Meta:
        ordering = ['-created_timestamp']

    def __str__(self):
        return self.branch_name
    
class Test(models.Model):
    id = models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} {self.name}"