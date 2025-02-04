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
    path('contact-us/', views.ContactUsCreateView.as_view(), name='contact-us'),
    path('about-us/', views.AboutUsTemplateView.as_view(), name='about-us'),
    path('user-post/list/' , views.UserPostListViewView.as_view(), name='user-posts'),
     path("api/v1/", include("account.api.v1.urls")),
]
