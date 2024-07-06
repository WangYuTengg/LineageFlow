# Generated by Django 5.0.6 on 2024-07-06 16:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
            ],
            options={
                "ordering": ["-created_timestamp"],
            },
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("url", models.URLField()),
                ("meta_data", models.TextField()),
                ("version", models.IntegerField(default=1)),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
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
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
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
                ("repo_name", models.CharField(max_length=100)),
                ("description", models.TextField(null=True)),
                ("default_branch", models.CharField(max_length=100)),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                ("updated_timestamp", models.DateTimeField(auto_now=True)),
                ("bucket_url", models.URLField(null=True)),
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
                ("commit_message", models.TextField(null=True)),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commits",
                        to="myapp.branch",
                    ),
                ),
                (
                    "add",
                    models.ManyToManyField(
                        default=[], related_name="add_set", to="myapp.file"
                    ),
                ),
                (
                    "edit",
                    models.ManyToManyField(
                        default=[], related_name="edit_set", to="myapp.file"
                    ),
                ),
                (
                    "remove",
                    models.ManyToManyField(
                        default=[], related_name="remove_set", to="myapp.file"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_timestamp"],
            },
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
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "commit",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meta_range",
                        to="myapp.commit",
                    ),
                ),
                (
                    "ranges",
                    models.ManyToManyField(
                        default=[], related_name="metaranges", to="myapp.range"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="file",
            name="metarange",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="myapp.metarange",
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="range",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="myapp.range",
            ),
        ),
        migrations.AddField(
            model_name="branch",
            name="repo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="branches",
                to="myapp.repo",
            ),
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
                ("username", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("created_timestamp", models.DateTimeField(auto_now_add=True)),
                ("email", models.EmailField(max_length=254)),
                ("repos", models.ManyToManyField(default=[], to="myapp.repo")),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="file",
            unique_together={("url", "metarange")},
        ),
    ]
