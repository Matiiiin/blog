import pytest
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import CommentReply


@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("post")
@pytest.mark.usefixtures("comment")
class TestCommentReplyView(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="password")
        self.url = reverse(
            "blog:comment-reply-create",
            kwargs={"comment_id": self.comment.id},
        )
        self.data = {"content": "Test Comment Reply"}

    def test_comment_reply_view_url(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)

    def test_comment_reply_creation(self):
        self.client.post(self.url, self.data)
        self.assertTrue(
            CommentReply.objects.filter(
                comment=self.comment,
                author=self.user.profile,
                content="Test Comment Reply",
            ).exists()
        )

    def test_comment_reply_redirect(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(
            response,
            reverse(
                "blog:post-detail",
                kwargs={"slug": self.comment.post.slug},
            ),
        )
