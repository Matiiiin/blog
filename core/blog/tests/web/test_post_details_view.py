import pytest
from django.test import TestCase, Client
from django.urls import reverse

@pytest.mark.usefixtures("user")
@pytest.mark.usefixtures("category")
@pytest.mark.usefixtures("post")
class TestPostDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('blog:post-detail', kwargs={'slug': self.post.slug})

    def test_post_detail_view_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'blog/post_detail_page/main.html')

    def test_post_detail_view_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['post'], self.post)
        self.assertIn('comment_form', response.context)
        self.assertIn('popular_posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('more_posts', response.context)