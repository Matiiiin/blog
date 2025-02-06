from django.core.management.base import BaseCommand, CommandError
from django.db.models import signals
from django.db import connection
from blog.models import Category


class Command(BaseCommand):
    help = "Creates categories"

    def handle(self, *args, **options):
        self.flush_table(Category)
        self.create_categories()

    def flush_table(self, model):
        self.stdout.write("Flushing data from Category table...\n")
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"
            )

    def create_categories(self):
        try:
            categories = [
                {
                    "name": "Travel",
                    "description": "Travel related posts",
                },
                {
                    "name": "Technology",
                    "description": "Technology related posts",
                },
                {"name": "Food", "description": "Food related posts"},
                {
                    "name": "Fashion",
                    "description": "Fashion related posts",
                },
                {
                    "name": "Health",
                    "description": "Health related posts",
                },
                {
                    "name": "Sports",
                    "description": "Sports related posts",
                },
                {
                    "name": "Music",
                    "description": "Music related posts",
                },
                {
                    "name": "Movies",
                    "description": "Movies related posts",
                },
                {
                    "name": "Books",
                    "description": "Books related posts",
                },
                {"name": "Art", "description": "Art related posts"},
                {
                    "name": "Science",
                    "description": "Science related posts",
                },
                {
                    "name": "Business",
                    "description": "Business related posts",
                },
                {
                    "name": "Education",
                    "description": "Education related posts",
                },
                {
                    "name": "Politics",
                    "description": "Politics related posts",
                },
                {
                    "name": "History",
                    "description": "History related posts",
                },
                {
                    "name": "Religion",
                    "description": "Religion related posts",
                },
                {
                    "name": "Nature",
                    "description": "Nature related posts",
                },
                {
                    "name": "Lifestyle",
                    "description": "Lifestyle related posts",
                },
                {
                    "name": "Entertainment",
                    "description": "Entertainment related posts",
                },
                {
                    "name": "Gaming",
                    "description": "Gaming related posts",
                },
                {
                    "name": "Culture",
                    "description": "Gaming related posts",
                },
            ]
            for category in categories:
                Category.objects.create(**category)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Category {category['name']} created successfully"
                    )
                )
        except Exception as e:
            raise CommandError(f"Error: {e}")
