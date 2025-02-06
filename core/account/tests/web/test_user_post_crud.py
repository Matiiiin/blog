import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Image
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("post")
class TestUserPostListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:user-posts")
        self.client.login(username="testuser", password="password")

    def test_user_post_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    #
    def test_user_post_list_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "account/dashboard/user_posts.html"
        )

    def test_user_post_list_view_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertFalse(response.context["is_paginated"])

    def test_user_post_list_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn("posts", response.context)
        self.assertEqual(response.context["posts"].count(), 1)


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("image_file")
@pytest.mark.usefixtures("category")
class TestUserPostCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:user-post-create")
        self.client.login(username="testuser", password="password")

    def test_user_post_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_post_create_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "account/dashboard/user_post_create.html"
        )

    def test_user_post_create_view_form_valid(self):
        image_file_1 = SimpleUploadedFile(
            "test_image_1.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        image_file_2 = SimpleUploadedFile(
            "test_image_2.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        image_file_3 = SimpleUploadedFile(
            "test_image_3.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        images = [image_file_1, image_file_2, image_file_3]
        data = {
            "category": self.category.id,
            "title": "Test Post",
            "hero_image": self.image_file,
            "short_content": "Short content",
            "main_content": "Main content",
            "images": images,
        }
        response = self.client.post(
            self.url, data, format="multipart", follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Post.objects.filter(title="Test Post").exists()
        )
        post = Post.objects.get(title="Test Post")
        self.assertEqual(post.author, self.user.profile)
        self.assertEqual(post.images.count(), 3)


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("post")
@pytest.mark.usefixtures("category")
class TestUserPostUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse(
            "account:user-post-update", kwargs={"slug": "test-post"}
        )
        self.client.login(username="testuser", password="password")

    def test_user_post_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_post_update_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "account/dashboard/user_post_update.html"
        )

    def test_user_post_update_view_form_valid(self):
        image_file_1 = SimpleUploadedFile(
            "test_image_1.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        image_file_2 = SimpleUploadedFile(
            "test_image_2.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        image_file_3 = SimpleUploadedFile(
            "test_image_3.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        images = [image_file_1, image_file_2, image_file_3]
        data = {
            "category": self.category.id,
            "title": "Updated Test Post",
            "short_content": "Updated short content",
            "main_content": "Updated main content",
            "images": images,
        }
        response = self.client.post(
            self.url, data, format="multipart", follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertTrue(
            Post.objects.filter(title="Updated Test Post").exists()
        )
        post = Post.objects.get(title="Updated Test Post")
        self.assertEqual(post.author, self.user.profile)
        self.assertEqual(post.images.count(), 3)


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("post")
class TestUserPostDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse(
            "account:user-post-delete", kwargs={"slug": "test-post"}
        )
        self.client.login(username="testuser", password="password")

    def test_user_post_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_post_delete_view_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "account/dashboard/user_post_delete.html"
        )

    def test_user_post_delete_view_post_deleted(self):
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse("account:user-posts"))
        self.assertFalse(
            Post.objects.filter(slug="test-post").exists()
        )
