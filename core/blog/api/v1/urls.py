from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
app_name = 'api-v1'
router = DefaultRouter()
router.register('image', views.ImageGenericViewSet, basename='image')
router.register('category', views.CategoryModelViewSet, basename='category')
router.register('comment', views.CommentModelViewSet, basename='comment')
router.register('comment-reply', views.CommentReplyModelViewSet, basename='comment-reply')
urlpatterns = [
    path('post/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('post/<slug:slug>', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
]
urlpatterns += router.urls