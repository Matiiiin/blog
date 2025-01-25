from django.urls import path , include
from account import views

app_name = 'account'

urlpatterns = [
    path('register/' , views.RegisterCreateView.as_view() , name='user-register'),
    path('login/' , views.LoginFormView.as_view() , name='user-login'),
    path('logout/' , views.LogoutView.as_view() , name='user-logout'),
    path('dashboard/' , views.UserDashboardTemplateView.as_view() , name='user-dashboard')
]