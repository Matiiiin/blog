from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from account.models import User
import jwt


class TestEmailConfirmationView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
        )
        self.user.is_verified = False
        self.user.save()
        self.token = jwt.encode(
            {"user_id": self.user.id},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    def test_valid_token(self):
        response = self.client.get(
            reverse("account:email-confirmation", args=[self.token])
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_verified)

    def test_already_verified_user(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.get(
            reverse("account:email-confirmation", args=[self.token])
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_token(self):
        invalid_token = "invalidtoken"
        response = self.client.get(
            reverse(
                "account:email-confirmation", args=[invalid_token]
            )
        )
        self.assertEqual(response.status_code, 400)

    def test_expired_token(self):
        expired_token = jwt.encode(
            {"user_id": self.user.id, "exp": 0},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        response = self.client.get(
            reverse(
                "account:email-confirmation", args=[expired_token]
            )
        )
        self.assertEqual(response.status_code, 400)

    def test_exception_handling(self):
        with self.settings(SECRET_KEY="wrongkey"):
            response = self.client.get(
                reverse(
                    "account:email-confirmation", args=[self.token]
                )
            )
            self.assertEqual(response.status_code, 400)


class TestEmailVerificationResendFormView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password",
        )
        self.user.is_verified = False
        self.user.save()

    def test_form_valid(self):
        response = self.client.post(
            reverse("account:email-activation-resend-form"),
            {"email": "testuser@example.com"},
        )
        self.assertEqual(response.status_code, 302)

    def test_form_invalid_email_not_exist(self):
        response = self.client.post(
            reverse("account:email-activation-resend-form"),
            {"email": "nonexistent@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Account associated to this email does not exist",
        )

    def test_form_invalid_already_verified(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.post(
            reverse("account:email-activation-resend-form"),
            {"email": "testuser@example.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account is already verified")
