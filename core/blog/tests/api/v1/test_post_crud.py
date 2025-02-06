import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from blog.models import Post


@pytest.mark.django_db
class TestPostListCreateAPIView:
    url = reverse('blog:api-v1:post-list-create')
    def test_anonymous_user(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    def test_list_posts(self, api_client, post ,user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_post(self, api_client, user, category, image ,image_file):
        api_client.force_authenticate(user=user)
        data = {
            'title': 'New Post',
            'category': category.id,
            'images': [image.id],
            'hero_image': image_file,
            'short_content': 'New short content',
            'main_content': 'New main content'
        }
        response = api_client.post(self.url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Post'
        assert Post.objects.filter(title='New Post').exists()
@pytest.mark.django_db
class TestPostRetrieveUpdateDestroyAPIView:

    def test_anonymous_user(self, api_client, post):
        response = api_client.get(reverse('blog:api-v1:post-retrieve-update-destroy',kwargs={'slug': post.slug}))
        assert response.status_code == status.HTTP_403_FORBIDDEN
    def test_retrieve_post(self, api_client, post , user):
        api_client.force_authenticate(user=user)
        response = api_client.get(reverse('blog:api-v1:post-retrieve-update-destroy',kwargs={'slug': post.slug}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title

    def test_update_post(self, api_client, user, post):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:post-retrieve-update-destroy',kwargs={'slug': post.slug})
        data = {
            'title': 'Updated Post',
            'short_content': 'Updated short content',
            'main_content': 'Updated main content'
        }
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.title == 'Updated Post'

    def test_delete_post(self, api_client, user, post):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:post-retrieve-update-destroy',kwargs={'slug': post.slug})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.count() == 0
        assert Post.objects.filter(title=post.title).exists() is False