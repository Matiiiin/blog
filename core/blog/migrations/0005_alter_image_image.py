# Generated by Django 5.1.5 on 2025-02-04 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(
                unique=True, upload_to="posts/images/"
            ),
        ),
    ]
