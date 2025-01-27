from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email(subject, from_email, recipient_list , template, message=None):
    email_body = template if template else message
    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        to=recipient_list,
    )
    if template:
        email.content_subtype = "html"
    email.send()