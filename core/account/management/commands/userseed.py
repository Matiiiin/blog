from django.core.management.base import BaseCommand, CommandError
from django.db.models import signals
from django.contrib.auth import get_user_model
from account.signals import create_profile_for_user
from django.db import connection
from account.models import Profile
User = get_user_model()

class Command(BaseCommand):
    help = "Creates users"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        self.flush_table(User)
        self.create_users()


    def flush_table(self ,model):
        self.stdout.write('Flushing data from User table...\n')
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
    def create_users(self):
        try:
            signals.post_save.disconnect(sender=User, receiver=create_profile_for_user)
            accounts = [
                {
                    "username": "admin",
                    "email": "admin@admin.com",
                    "password": "asd",
                    "is_superuser": True,
                    "is_staff": True,
                    "is_active": True,
                    "is_verified": True,
                },
                {
                    "username": "johndoe",
                    "email": "john@example.com",
                    "password": "asd",
                    "is_superuser": False,
                    "is_staff": True,
                    "is_active": True,
                    "is_verified": True,
                },
                {
                    "username": "janesmith",
                    "email": "jane@example.com",
                    "password": "asd",
                    "is_superuser": False,
                    "is_staff": False,
                    "is_active": True,
                    "is_verified": True,
                }
            ]

            account_profiles = [
                {
                    "user_id": 1,
                    "first_name": "Admin",
                    "last_name": "Admin",
                    "bio": "I am the admin of this site. I have full control over all the features and functionalities of this site. If you have any questions or concerns, feel free to contact me.",
                    "image": "account/profile/default.jpg",
                },
                {
                    "user_id": 2,
                    "first_name": "John",
                    "last_name": "Doe",
                    "bio": "I am a dedicated software developer with 5 years of experience. I specialize in backend development and database management. I am passionate about learning new technologies and improving my coding skills. In my free time, I enjoy contributing to open-source projects.",
                    "image": "account/profile/johndoe.jpg",
                },
                {
                    "user_id": 3,
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "bio": "I am an experienced project manager and team leader. I have a strong background in agile methodologies and project planning. I excel at coordinating cross-functional teams and ensuring project success. Outside of work, I enjoy mentoring young professionals.",
                    "image": "account/profile/janesmith.jpg",
                },
            ]
            for account in accounts:
                user = User.objects.create(**account)
                user.set_password(account["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User {user.username} created successfully"))
            for account_profile in account_profiles:
                profile = Profile.objects.create(**account_profile)
                self.stdout.write(self.style.SUCCESS(f"Profile for {profile.user} created successfully"))
            signals.post_save.connect(sender=User, receiver=create_profile_for_user)

        except Exception as e:
            raise CommandError(f"Error: {e}")


