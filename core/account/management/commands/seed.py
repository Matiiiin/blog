from django.core.management.base import BaseCommand, CommandError
from .userseed import Command as UserSeed
from blog.management.commands.categoryseed import (
    Command as CategorySeed,
)
from blog.management.commands.commentseed import (
    Command as CommentSeed,
)
from blog.management.commands.postseed import Command as PostSeed


class Command(BaseCommand):
    help = "Creates categories"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("seeding data..."))
        UserSeed().handle()
        CategorySeed().handle()
        PostSeed().handle()
        CommentSeed().handle()
        self.stdout.write(self.style.WARNING("seeding done"))
