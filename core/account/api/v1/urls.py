from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api-v1"
router = DefaultRouter()
router.register("auth", views.AuthGenericViewSet, basename="auth")

urlpatterns = [
    path(
        "token-auth-login/",
        views.CustomAuthTokenLogin.as_view(),
        name="token-auth-login",
    ),
    path(
        "token-auth-logout/",
        views.CustomAuthTokenLogout.as_view(),
        name="token-auth-logout",
    ),
    path(
        "jwt-create/",
        TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path(
        "jwt-refresh/", TokenRefreshView.as_view(), name="jwt-refresh"
    ),
]
urlpatterns += router.urls
