import pytest
from rest_framework import status
from django.urls import reverse
from blog.models import Category


@pytest.mark.django_db
class TestCategoryModelViewSet:

    def test_list_categories(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:category-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_category(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_create_category(self, api_client, user):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:category-list")
        data = {
            "name": "NewCategory",
            "description": "New Description",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_can_update_category(
        self, api_client, user, category
    ):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        data = {
            "name": "UpdatedCategory",
            "description": "Updated Description",
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_partial_update_category(
        self, api_client, user, category
    ):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        data = {"name": "PartiallyUpdatedCategory"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_category(
        self, api_client, user, category
    ):
        user.is_staff = True
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_category_non_admin(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("blog:api-v1:category-list")
        data = {
            "name": "NewCategory",
            "description": "New Description",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_category_non_admin(
        self, api_client, user, category
    ):
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        data = {
            "name": "UpdatedCategory",
            "description": "Updated Description",
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_non_admin(
        self, api_client, user, category
    ):
        api_client.force_authenticate(user=user)
        url = reverse(
            "blog:api-v1:category-detail", args=[category.id]
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
