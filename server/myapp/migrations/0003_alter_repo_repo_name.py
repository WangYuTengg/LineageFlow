# Generated by Django 4.2.13 on 2024-07-04 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_rename_name_users_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repo", name="repo_name", field=models.CharField(max_length=100),
        ),
    ]