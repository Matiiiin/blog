import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from account.models import User, Profile


class TestAboutUsTemplateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:about-us")
        self.user = User.objects.create_user(
            username="testuser",
            email="matinnjt2000@gmail.com",
            password="password",
        )

    def test_about_us_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_us_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "account/about_us.html")

    def test_about_us_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("images", response.context)
        self.assertIn("team", response.context)
        expected_images = [
            settings.MEDIA_URL + "about_us/hero_1.jpg",
            settings.MEDIA_URL + "about_us/hero_2.jpg",
            settings.MEDIA_URL + "about_us/hero_5.jpg",
            settings.MEDIA_URL + "about_us/img_7_sq.jpg",
        ]
        self.assertEqual(response.context["images"], expected_images)
        self.assertEqual(response.context["team"], self.user.profile)
