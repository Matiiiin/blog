import json
import sys
from rest_framework.test import APIClient, force_authenticate
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        username="test", email="tests@tests.com", password="123"
    )
    return user


@pytest.mark.django_db
class TestVerifyAccountResendRequestApi:
    url = reverse("account:api-v1:auth-verification-resend")

    def test_verify_account_resend_api_with_valid_data(
        self, api_client, common_user
    ):
        data = {"email": "tests@tests.com"}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 200

    def test_verify_account_resend_api_with_invalid_data(
        self, api_client, common_user
    ):
        data = {"email": "test2@tests.com"}
        response = api_client.post(self.url, data=data)
        assert response.status_code == 404
