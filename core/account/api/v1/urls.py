from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'account:api:v1'
router = DefaultRouter()
router.register('auth', views.AuthGenericViewSet, basename='auth')

urlpatterns = [
    path('token-auth/', views.CustomAuthToken.as_view(), name='token_auth'),
    path('jwt-create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns+=router.urls