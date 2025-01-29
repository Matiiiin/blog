import pytest
from rest_framework import status
from django.urls import reverse
from blog.models import Comment, CommentReply
from account.models import User

@pytest.mark.django_db
class TestCommentModelViewSet:

    def test_list_comments(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_comment(self, api_client, user, comment):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_comment(self, api_client, user, post):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-list')
        data = {'content': 'New Comment', 'post': post.slug}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_comment(self, api_client, user, comment , post):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        data = {
            'content': 'Updated Comment',
            'post':post.slug
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_partial_update_comment(self, api_client, user, comment):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        data = {'content': 'Partially Updated Comment'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_comment(self, api_client, user, comment):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_comment_non_verified(self, api_client, user, post):
        user.is_verified = False
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-list')
        data = {'content': 'New Comment', 'post': post.slug}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_comment_non_owner(self, api_client, user, comment):
        non_owner_user = User.objects.create_user(username='non_owner',email='non_owner@test.com', password='non_owner')
        comment.author = non_owner_user.profile
        comment.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        data = {'content': 'Updated Comment'}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_comment_non_owner(self, api_client, user, comment):
        non_owner_user = User.objects.create_user(username='non_owner',email='non_owner@test.com', password='non_owner')
        comment.author = non_owner_user.profile
        comment.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-detail', args=[comment.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestCommentReplyModelViewSet:

    def test_list_comment_replies(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_comment_reply(self, api_client, user, comment_reply):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_comment_reply(self, api_client, user, comment):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-list')
        data = {'content': 'New Comment Reply', 'comment': comment.id}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_comment_reply(self, api_client, user, comment_reply):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        data = {'content': 'Updated Comment Reply' , 'comment': comment_reply.comment.id}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_partial_update_comment_reply(self, api_client, user, comment_reply):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        data = {'content': 'Partially Updated Comment Reply'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_comment_reply(self, api_client, user, comment_reply):
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_comment_reply_non_verified(self, api_client, user, comment):
        user.is_verified = False
        user.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-list')
        data = {'content': 'New Comment Reply', 'comment': comment.id}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_comment_reply_non_owner(self, api_client, user, comment_reply):
        non_owner_user = User.objects.create_user(username='non_owner',email='non_owner@test.com', password='non_owner')
        comment_reply.author = non_owner_user.profile
        comment_reply.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        data = {'content': 'Updated Comment Reply'}
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_comment_reply_non_owner(self, api_client, user, comment_reply):
        non_owner_user = User.objects.create_user(username='non_owner',email='non_owner@test.com', password='non_owner')
        comment_reply.author = non_owner_user.profile
        comment_reply.save()
        api_client.force_authenticate(user=user)
        url = reverse('blog:api-v1:comment-reply-detail', args=[comment_reply.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN