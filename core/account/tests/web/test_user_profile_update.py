import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from account.forms import UserProfileUpdateForm
import pytest

User = get_user_model()

@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("image_file")
class TestUserProfileUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:user-profile-update")
        self.client.login(username="testuser", password="password")

    def test_user_profile_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_update_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "account/dashboard/user_settings.html")

    def test_user_profile_update_view_form_valid(self):
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "email": "newemail@example.com",
            "username": "newusername",
            "password": "newpassword",
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "bio": "New bio",
            "image": self.image_file,
        }
        response = self.client.post(self.url, data, follow=True)
        self.user.refresh_from_db()
        user = User.objects.get(username="newusername")
        self.assertEqual(user.email, "newemail@example.com")
        self.assertTrue(user.check_password("newpassword"))
        self.assertEqual(user.profile.first_name, "NewFirstName")
        self.assertEqual(user.profile.last_name, "NewLastName")
        self.assertEqual(user.profile.bio, "New bio")
        self.assertIsNotNone(user.profile.image)