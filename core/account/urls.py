from django.urls import path, include
from account import views

app_name = "account"
urlpatterns = [
    path(
        "register/",
        views.RegisterCreateView.as_view(),
        name="user-register",
    ),
    path(
        "email-verification-resend-form/",
        views.EmailVerificationResendFormView.as_view(),
        name="email-activation-resend-form",
    ),
    path(
        "email-confirmation/<str:token>",
        views.EmailConfirmationView.as_view(),
        name="email-confirmation",
    ),
    path(
        "forgot-password/",
        views.ForgotPasswordFormView.as_view(),
        name="forgot-password",
    ),
    path(
        "forgot-password-confirmation/<str:token>",
        views.ForgotPasswordConfirmFormView.as_view(),
        name="forgot-password-confirmation",
    ),
    path("login/", views.LoginFormView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    path(
        "dashboard/",
        views.UserDashboardTemplateView.as_view(),
        name="user-dashboard",
    ),
    path(
        "contact-us/",
        views.ContactUsCreateView.as_view(),
        name="contact-us",
    ),
    path(
        "about-us/",
        views.AboutUsTemplateView.as_view(),
        name="about-us",
    ),
    path(
        "user-post/list/",
        views.UserPostListView.as_view(),
        name="user-posts",
    ),
    path(
        "user-post/create/",
        views.UserPostCreateView.as_view(),
        name="user-post-create",
    ),
    path(
        "user-post/update/<slug:slug>",
        views.UserPostUpdateView.as_view(),
        name="user-post-update",
    ),
    path(
        "user-post/delete/<slug:slug>",
        views.UserPostDeleteView.as_view(),
        name="user-post-delete",
    ),
    path(
        "user-profile/update/",
        views.UserProfileUpdateView.as_view(),
        name="user-profile-update",
    ),
    path("api/v1/", include("account.api.v1.urls")),
]
