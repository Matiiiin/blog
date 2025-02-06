from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User, Profile, ContactUs
from .tasks import send_email

"""
save a profile for the created user
"""


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.username,
        )


@receiver(post_save, sender=ContactUs)
def send_email_contact_us_message_to_admin(
    sender, instance, created, **kwargs
):
    if created:
        send_email.delay(
            subject="A new Contact Us messaege is creted",
            from_email="matinnejatbakhshdev@gmail.com",
            recipient_list=["matinnejatbakhshdev@gmail.com"],
            message=f"<p>Name:{instance.name} <br> Email:{instance.email}"
            f"<br> Subject:{instance.subject}"
            f"<br> Message:{instance.message}</p>",
        )
