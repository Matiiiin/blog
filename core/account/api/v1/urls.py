from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
app_name = 'account:api:v1'
router = DefaultRouter()
router.register('auth', views.AuthGenericViewSet, basename='auth')

urlpatterns = [
]
urlpatterns+=router.urls