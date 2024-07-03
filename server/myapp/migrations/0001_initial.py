# Generated by Django 4.2.13 on 2024-07-03 15:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Files",
            fields=[
                ("url", models.URLField(primary_key=True, serialize=False)),
                ("meta_data", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Repo",
            fields=[
                (
                    "repo_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("repo_name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(null=True)),
                ("default_branch", models.CharField(max_length=100)),
                ("bucket_url", models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "user_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("repos", models.ManyToManyField(default=[], to="myapp.repo")),
            ],
        ),
        migrations.CreateModel(
            name="UserToRepo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(default="admin", max_length=100)),
                (
                    "repo_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repo_user",
                        to="myapp.repo",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to="myapp.users",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Range",
            fields=[
                (
                    "range_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("files", models.ManyToManyField(to="myapp.files")),
            ],
        ),
        migrations.CreateModel(
            name="MetaRange",
            fields=[
                (
                    "meta_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("ranges", models.ManyToManyField(default=[], to="myapp.range")),
            ],
        ),
        migrations.CreateModel(
            name="Commit",
            fields=[
                (
                    "commit_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "add",
                    models.ManyToManyField(
                        default=[], related_name="add_set", to="myapp.files"
                    ),
                ),
                (
                    "edit",
                    models.ManyToManyField(
                        default=[], related_name="edit_set", to="myapp.files"
                    ),
                ),
                (
                    "meta_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.metarange",
                    ),
                ),
                (
                    "remove",
                    models.ManyToManyField(
                        default=[], related_name="remove_set", to="myapp.files"
                    ),
                ),
            ],
            options={"ordering": ["-timestamp"],},
        ),
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "branch_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("branch_name", models.CharField(max_length=100)),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                ("updated_timestamp", models.DateTimeField(auto_now=True)),
                (
                    "commit_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commits",
                        to="myapp.commit",
                    ),
                ),
                (
                    "repo_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repo",
                        to="myapp.repo",
                    ),
                ),
            ],
            options={"ordering": ["-created_timestamp"],},
        ),
    ]
