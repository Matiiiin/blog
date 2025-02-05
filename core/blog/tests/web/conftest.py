import pytest
from rest_framework.test import APIClient
from blog.models import Post, Category, Image , Comment , CommentReply
from account.models import Profile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
User = get_user_model()

@pytest.fixture(scope="class")
def user(request):
    user = User.objects.create_user(username='testuser',email='testuser@test.com', password='password' , is_verified=True)
    request.cls.user = user
    return user

@pytest.fixture(scope="class")
def category(request):
    category = Category.objects.create(name='TestCategory', description='Test Description')
    request.cls.category = category
    return category

@pytest.fixture(scope="class")
def image(request):
    image = Image.objects.create(image='test_image.jpg')
    request.cls.image = image
    return image
@pytest.fixture(scope="class")
def post(request, user, category, image):
    post = Post.objects.create(
        author=user.profile,
        category=category,
        title='Test Post',
        hero_image='test_hero_image.jpg',
        short_content='Short content',
        main_content='Main content'
    )
    post.images.add(image)
    request.cls.post = post
    return post

@pytest.fixture(scope="class")
def comment(request, user, post):
    comment = Comment.objects.create(author=user.profile, post=post, content='Test Comment')
    request.cls.comment = comment
    return comment
@pytest.fixture(scope="class")
def comment_reply(request, user, comment):
    reply = CommentReply.objects.create(author=user.profile, comment=comment, content='Test Comment Reply')
    request.cls.reply = reply
    return reply
@pytest.fixture(scope="class")
def image_file(request):
    image_file =  SimpleUploadedFile(name='test_image.jpg',
                                  content=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="),
                                  content_type='image/jpeg')
    request.cls.image_file = image_file
    return image_file