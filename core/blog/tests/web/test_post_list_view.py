import pytest
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("category")
@pytest.mark.usefixtures("post")
class TestPostListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("blog:post-list")

    def test_post_list_view_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "blog/post_list_page/main.html"
        )

    def test_post_list_view_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue("is_paginated" in response.context)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["posts"]), 1)

    def test_post_list_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("popular_posts", response.context)
        self.assertIn("categories", response.context)
        self.assertEqual(len(response.context["posts"]), 1)
