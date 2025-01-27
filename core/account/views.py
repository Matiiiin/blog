from django.shortcuts import render
from django.views.generic import TemplateView , FormView , CreateView , View
from account.models import User
from .forms import LoginForm ,UserRegistrationForm , EmailVerificationResendForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate , login ,logout
from django.http import HttpResponse , HttpResponseBadRequest , HttpResponseRedirect
import logging
from django.core.mail import EmailMessage
from .task import send_email
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.shortcuts import get_object_or_404
from django.conf import settings
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
            token = RefreshToken.for_user(user)
            #send activation email
            email_verification_template= render_to_string('account/email_verification.html' , {'user':user , 'token':token})
            send_email.delay(
                subject = 'Welcome to our blog' ,
                message = 'Thank you for registering' ,
                from_email = 'noreply@blog.com' ,
                recipient_list = [user.email],
                template = email_verification_template
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(f'Exception in Register, details:{e}')
            return HttpResponseBadRequest('Sorry there was an error , please try again')
class EmailConfirmationView(View):
    def get(self , request , token):
        try:
            user_id = jwt.decode(token , settings.SECRET_KEY , algorithms=['HS256'])['user_id']
            user = get_object_or_404(User , pk = user_id)
            if user.is_verified:
                return HttpResponse('User already verified')
            user.is_verified = True
            user.save()
            return HttpResponseRedirect(reverse_lazy('account:user-login'))
        except jwt.exceptions.DecodeError:
            return HttpResponseBadRequest('Invalid token')
        except jwt.ExpiredSignatureError:
            return HttpResponseBadRequest('Token expired')
        except Exception as e:
            logger.error(f'Exception in Register Confirmation, details:{e}')
            return HttpResponseBadRequest('Sorry there was an error , please try again')
class EmailVerificationResendFormView(FormView):
    form_class = EmailVerificationResendForm
    template_name = 'account/email_verification_resend-form.html'
    success_url = reverse_lazy('account:user-login')
    def form_valid(self, form):
        try:
            user = form.cleaned_data.get('user')
            token = RefreshToken.for_user(user)
            email_verification_template = render_to_string('account/email_verification_resend.html' , {'user':user , 'token':token})
            send_email.delay(
                subject = 'Account verification' ,
                from_email = 'noreply@blog.com',
                recipient_list = [user.email],
                template = email_verification_template
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(f'Exception in Email Verification Resend, details:{e}')
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