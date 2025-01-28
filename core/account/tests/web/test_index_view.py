from django.test import TestCase
from django.urls import reverse


class TestHomePageTemplateView(TestCase):
    def test_home_page_template_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
