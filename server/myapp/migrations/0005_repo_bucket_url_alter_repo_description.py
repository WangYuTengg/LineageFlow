# Generated by Django 4.2.13 on 2024-07-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_branch_repo_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="repo", name="bucket_url", field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="repo", name="description", field=models.TextField(null=True),
        ),
    ]
