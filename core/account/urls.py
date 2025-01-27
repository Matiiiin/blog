from django.urls import path , include
from account import views

app_name = 'account'
urlpatterns = [
    path('register/' , views.RegisterCreateView.as_view() , name='user-register'),
    path('email-verification-resend-form/' , views.EmailVerificationResendFormView.as_view() , name='email-activation-resend-form'),
    # path('user-activation-email-resend/' , views.RegisterActivationResendEmailView.as_view() , name='user-activation-email-resend'),
    path('email-confirmation/<str:token>' , views.EmailConfirmationView.as_view() , name='email-confirmation'),
    path('login/' , views.LoginFormView.as_view() , name='user-login'),
    path('logout/' , views.LogoutView.as_view() , name='user-logout'),
    path('dashboard/' , views.UserDashboardTemplateView.as_view() , name='user-dashboard')
]

