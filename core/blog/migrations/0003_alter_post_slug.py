# Generated by Django 5.1.5 on 2025-01-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_remove_tag_posts_post_tags_alter_post_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=100),
        ),
    ]
