from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestUserDashboardTemplateView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password",
            email="testuser@example.com",
        )

    def test_dashboard_view_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("account:user-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile", response.context)

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse("account:user-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('account:user-login')}?next={reverse('account:user-dashboard')}",
        )
