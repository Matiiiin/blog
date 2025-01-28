from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class TestForgotPasswordConfirmFormView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="old_password",
        )
        self.token = str(RefreshToken.for_user(self.user))
        self.url = reverse(
            "account:forgot-password-confirmation",
            kwargs={"token": self.token},
        )

    def test_valid_password_change(self):
        new_password = "new_password123"
        response = self.client.post(
            self.url,
            {
                "current_password": "old_password",
                "new_password": new_password,
                "new_password_confirm": new_password,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_invalid_current_password(self):
        new_password = "new_password123"
        response = self.client.post(
            self.url,
            {
                "current_password": "wrong_password",
                "new_password": new_password,
                "new_password_confirm": new_password,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current password is incorrect")

    def test_passwords_do_not_match(self):
        response = self.client.post(
            self.url,
            {
                "current_password": "old_password",
                "new_password": "new_password123",
                "new_password_confirm": "different_password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")

    def test_invalid_token(self):
        invalid_token = jwt.encode(
            {"user_id": self.user.id},
            "wrong_secret",
            algorithm="HS256",
        )
        url = reverse(
            "account:forgot-password-confirmation",
            kwargs={"token": invalid_token},
        )
        response = self.client.post(
            url,
            {
                "current_password": "old_password",
                "new_password": "new_password123",
                "new_password_confirm": "new_password123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid token")

    def test_expired_token(self):
        expired_token = jwt.encode(
            {"user_id": self.user.id, "exp": 0},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        url = reverse(
            "account:forgot-password-confirmation",
            kwargs={"token": expired_token},
        )
        response = self.client.post(
            url,
            {
                "current_password": "old_password",
                "new_password": "new_password123",
                "new_password_confirm": "new_password123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Token has expired")
