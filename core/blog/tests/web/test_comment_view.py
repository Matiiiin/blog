import pytest
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Comment


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("post")
class TestCommentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="password")
        self.url = reverse(
            "blog:comment-create",
            kwargs={"post_slug": self.post.slug},
        )
        self.data = {"content": "Test Comment"}

    def test_comment_view_url(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)

    def test_comment_creation(self):
        self.client.post(self.url, self.data)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post,
                author=self.user.profile,
                content="Test Comment",
            ).exists()
        )

    def test_comment_redirect(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(
            response,
            reverse(
                "blog:post-detail", kwargs={"slug": self.post.slug}
            ),
        )
