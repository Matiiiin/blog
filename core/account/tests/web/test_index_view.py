from django.test import TestCase
from django.urls import reverse
from blog.models import Post , Category
from account.models import User

class TestHomePageTemplateView(TestCase):

    def test_home_page_template_view(self):
        user = User.objects.create_user(
            username="testuser",
            email="testemail@gmail.com", password="testpassword")
        posts_categories = ['Technology' , 'Culture' , 'Travel' , 'Fashion']
        for category in posts_categories:
            cat= Category.objects.create(name=category)
            for i in range(20):
                post = Post.objects.create(
                    title=f"Post{category}_{i}",
                    short_content=f"Content{category}_{i}",
                    hero_image="default.jpg",
                    category=cat,
                    author=user.profile
                )
                post.save()
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
