import random

from django.core.management.base import BaseCommand, CommandError
from django.db.models import signals
from django.db import connection
from blog.models import Comment , CommentReply , Post
from account.models import Profile
from faker import Faker
fake = Faker()

class Command(BaseCommand):
    help = "Creates comments and comment replies for posts"
    def handle(self, *args, **options):
        self.flush_table(Comment , CommentReply)
        self.create_comments()


    def flush_table(self ,*model):

        self.stdout.write('Flushing data from Comment table...\n')
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {model[0]._meta.db_table} RESTART IDENTITY CASCADE')

        self.stdout.write('Flushing data from CommentReply table...\n')
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {model[1]._meta.db_table} RESTART IDENTITY CASCADE')
    def create_comments(self):
        try:
            posts = Post.objects.all()
            authors = Profile.objects.exclude(user__is_superuser=True)
            for post in posts:
                for i in range(1, 4):
                    comment = Comment.objects.create(post=post, author=random.choice(authors), content=fake.sentence(nb_words=50))
                    self.stdout.write(self.style.SUCCESS(f"Created comment: {comment.content}"))
                    for j in range(1, 4):
                        comment_reply = CommentReply.objects.create(comment=comment, author=random.choice(authors), content=fake.sentence(nb_words=50))
                        self.stdout.write(self.style.SUCCESS(f"Created comment reply: {comment_reply.content}"))
        except Exception as e:
            raise CommandError(f"Error: {e}")


