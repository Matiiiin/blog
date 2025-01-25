from django.shortcuts import render
from django.views.generic import TemplateView , FormView , CreateView , View
from account.models import User
from .forms import LoginForm ,UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate , login ,logout
from django.http import HttpResponse , HttpResponseBadRequest , HttpResponseRedirect
import logging
from django.core.mail import EmailMessage

# Create your views here.
logger = logging.getLogger(__name__)
class HomePageTemplateView(TemplateView):
    template_name = 'index.html'
class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name_suffix = '_register'
    success_url = reverse_lazy('account:user-login')
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('account:user-dashboard'))
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        try:
            password = form.cleaned_data.get('password')
            user = form.save(commit = False)
            user.set_password(password)
            user.save()
            login(self.request , user)
            #send activation email
            email = EmailMessage(
                "Hello",
                "Body goes here",
                "noreply@blog.com",
                [user.email],
            )
            email.send()
            print(email)
            return super().form_valid(form)
        except Exception as e:
            logger.error(f'Exception in Register, details:{e}')
            return HttpResponseBadRequest('Sorry there was an error , please try again')

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'account/user_login.html'
    success_url = reverse_lazy('account:user-dashboard')
    def get(self , request , *args , **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request , *args , **kwargs)
    def form_valid(self, form):
        try:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password=password)
            login(self.request , user)
            return super().form_valid(form)
        except Exception as e:
            logger.error(f'Exception in Login, details:{e}')
            return HttpResponseBadRequest('Sorry there was an error , please try again')
class LogoutView(View):
    def get(self , request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('account:user-login'))

class UserDashboardTemplateView(TemplateView):
    template_name = 'account/user_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context