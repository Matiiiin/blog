import pytest
from rest_framework import status
from django.urls import reverse
from blog.models import Image

@pytest.mark.django_db
class TestImageGenericViewSet:

    def test_anonymous_user_image_list_create(self, api_client):
        url = reverse('blog:api-v1:image-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    def test_anonymous_user_image_retrieve_update_destroy(self, api_client, image):
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_images(self, api_client, user, image):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Image.objects.count()

    def test_retrieve_image(self, api_client, user, image):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == image.id

    def test_create_image(self, api_client, user, image_file):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-list')
        data = {'image': image_file}
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert Image.objects.filter(id=response.data['id']).exists()

    def test_normal_user_cant_update_image(self, api_client, user, image, image_file):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        data = {'image': image_file}
        response = api_client.put(url, data, format='multipart')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_update_image(self, api_client, user, image, image_file):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        data = {'image': image_file}
        response = api_client.put(url, data, format='multipart')
        assert response.status_code == status.HTTP_200_OK
        assert Image.objects.filter(id=image.id).exists()

    def test_normal_user_cant_delete_image(self, api_client, user, image):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_delete_image(self, api_client, user, image):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:image-detail', args=[image.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Image.objects.filter(id=image.id).exists()
