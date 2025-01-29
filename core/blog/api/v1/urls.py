from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
app_name = 'api-v1'
router = DefaultRouter()
router.register('image', views.ImageGenericViewSet, basename='image')
urlpatterns = [
    path('post/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('post/<slug:slug>', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
]
urlpatterns += router.urls