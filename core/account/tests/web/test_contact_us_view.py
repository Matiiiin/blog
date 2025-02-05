from django.test import TestCase, Client
from django.urls import reverse
from account.models import ContactUs

class TestContactUsCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:contact-us")

    def test_get_contact_us_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/contact_us.html")

    def test_post_valid_contact_us_form(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test User",
                "email": "testuser@example.com",
                "subject": "Test subject",
                "message": "This is a test message.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("homepage"))
        self.assertTrue(ContactUs.objects.filter(email="testuser@example.com").exists())
