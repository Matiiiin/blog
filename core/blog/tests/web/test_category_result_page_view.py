from django.test import TestCase, Client
from django.urls import reverse
import pytest


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("category")
@pytest.mark.usefixtures("post")
class TestCategoryResultTemplateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse(
            "blog:category-result",
            kwargs={"category_name": self.category.name},
        )

    def test_category_result_view_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_result_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "blog/category_result_page/main.html"
        )

    def test_category_result_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is False)
        self.assertEqual(len(response.context["category_posts"]), 1)

    def test_category_result_view_lists_all_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["category_posts"]), 1)

    def test_category_result_view_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["category_name"], self.category.name
        )
        self.assertIn("popular_posts", response.context)
        self.assertIn("categories", response.context)
