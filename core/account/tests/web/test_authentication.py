from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.forms import UserRegistrationForm
from blog.models import Post, Category


User = get_user_model()


class TestRegisterCreateView(TestCase):
    url = reverse("account:user-register")

    def test_get_authenticated_user_redirect(self):
        user = User.objects.create_user(
            username="test", email="test@test.com", password="123"
        )
        self.client.login(username="test", password="123")
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("account:user-dashboard")
        )

    def test_get_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "account/user_register.html"
        )

    def test_post_valid_data(self):
        response = self.client.post(
            self.url,
            {
                "username": "test",
                "email": "test@test.com",
                "password": "123",
                "password_confirm": "123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username="test").first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("123"))
        self.assertTrue(user.is_authenticated)

    def test_post_invalid_data(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "12345",
                "password_confirm": "54321",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Passwords do not match", count=1
        )

    def test_post_user_already_exists(self):
        User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="12345",
        )
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "12345",
                "password_confirm": "12345",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "User with this Username already exists",
            count=1,
        )


class TestLoginFormView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:user-login")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword",
            is_verified=True,
        )

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/user_login.html")

    def test_login_view_post_valid(self):
        response = self.client.post(
            self.url,
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertRedirects(
            response, reverse("account:user-dashboard")
        )

    def test_login_view_post_invalid_username(self):
        response = self.client.post(
            self.url,
            {"username": "wronguser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username")

    def test_login_view_post_invalid_password(self):
        response = self.client.post(
            self.url,
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid password")

    def test_login_view_authenticated_user_redirect(self):
        self.client.login(
            username="testuser", password="testpassword"
        )
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("account:user-dashboard")
        )


class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("account:user-logout")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword",
        )

    def test_logout_view_redirects(self):
        self.client.login(
            username="testuser", password="testpassword"
        )
        response = self.client.get(self.url)
        posts_categories = [
            "Technology",
            "Culture",
            "Travel",
            "Fashion",
        ]
        for category in posts_categories:
            cat = Category.objects.create(name=category)
            for i in range(20):
                post = Post.objects.create(
                    title=f"Post{category}_{i}",
                    short_content=f"Content{category}_{i}",
                    hero_image="default.jpg",
                    category=cat,
                    author=self.user.profile,
                )
                post.save()
        self.assertRedirects(response, reverse("homepage"))

    def test_logout_view_logs_out_user(self):
        self.client.login(
            username="testuser", password="testpassword"
        )
        self.client.get(self.url)
        response = self.client.get(reverse("account:user-dashboard"))
        self.assertRedirects(
            response,
            reverse("account:user-login")
            + "?next="
            + reverse("account:user-dashboard"),
        )
