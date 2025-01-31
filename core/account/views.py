from django.views.generic import (
    TemplateView,
    FormView,
    CreateView,
    View,
)
from account.models import User
from .forms import (
    LoginForm,
    UserRegistrationForm,
    EmailVerificationResendForm,
    ForgotPasswordForm,
    ForgotPasswordConfirmForm,
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
import logging
from .tasks import send_email
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.shortcuts import get_object_or_404
from django.conf import settings
from account.utils import make_random_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
logger = logging.getLogger(__name__)


class HomePageTemplateView(TemplateView):
    """
    Shows index view of website
    """

    template_name = "index.html"


class RegisterCreateView(CreateView):
    """
    Fill in the form and user is created in database
    """

    model = User
    form_class = UserRegistrationForm
    template_name_suffix = "_register"
    success_url = reverse_lazy("account:user-login")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy("account:user-dashboard")
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            password = form.cleaned_data.get("password")
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            login(self.request, user)
            token = RefreshToken.for_user(user)
            # send activation email
            email_verification_template = render_to_string(
                "account/email_verification.html",
                {"user": user, "token": token},
            )
            send_email.delay(
                subject="Welcome to our blog",
                message="Thank you for registering",
                from_email="noreply@blog.com",
                recipient_list=[user.email],
                template=email_verification_template,
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Exception in Register, details:{e}")
            return HttpResponseBadRequest(
                "Sorry there was an error , please try again"
            )


class EmailConfirmationView(View):
    """
    Verifies the user email
    """

    def get(self, request, token):
        try:
            user_id = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )["user_id"]
            user = get_object_or_404(User, pk=user_id)
            if user.is_verified:
                return HttpResponse("User already verified")
            user.is_verified = True
            user.save()
            return HttpResponseRedirect(
                reverse_lazy("account:user-login")
            )
        except jwt.exceptions.DecodeError:
            return HttpResponseBadRequest("Invalid token")
        except jwt.ExpiredSignatureError:
            return HttpResponseBadRequest("Token expired")
        except Exception as e:
            logger.error(
                f"Exception in Register Confirmation, details:{e}"
            )
            return HttpResponseBadRequest(
                "Sorry there was an error , please try again"
            )


class EmailVerificationResendFormView(FormView):
    """
    Shows the form for sending email
    """

    form_class = EmailVerificationResendForm
    template_name = "account/email_verification_resend-form.html"
    success_url = reverse_lazy("account:user-login")

    def form_valid(self, form):
        try:
            user = form.cleaned_data.get("user")
            token = RefreshToken.for_user(user)
            email_verification_template = render_to_string(
                "account/email_verification_resend.html",
                {"user": user, "token": token},
            )
            send_email.delay(
                subject="Account verification",
                from_email="noreply@blog.com",
                recipient_list=[user.email],
                template=email_verification_template,
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(
                f"Exception in Email Verification Resend, details:{e}"
            )
            return HttpResponseBadRequest(
                "Sorry there was an error , please try again"
            )


class LoginFormView(FormView):
    """
    A form for logging user in
    """

    form_class = LoginForm
    template_name = "account/user_login.html"
    success_url = reverse_lazy("account:user-dashboard")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Exception in Login, details:{e}")
            return HttpResponseBadRequest(
                "Sorry there was an error , please try again"
            )


class LogoutView(LoginRequiredMixin, View):
    """
    Logout the user
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class ForgotPasswordFormView(FormView):
    """
    A form for requesting a new password threw email
    """

    form_class = ForgotPasswordForm
    template_name = "account/forgot_password_form.html"
    success_url = reverse_lazy("account:user-login")

    def form_valid(self, form):
        try:
            user = form.cleaned_data.get("user")
            temp_password = make_random_string()
            user.set_password(temp_password)
            user.save()
            token = RefreshToken.for_user(user)
            email_forgot_password_template = render_to_string(
                "account/forgot_password.html",
                {
                    "user": user,
                    "temp_password": temp_password,
                    "token": str(token),
                },
            )
            send_email.delay(
                subject="Reset password",
                from_email="noreply@blog.com",
                recipient_list=[user.email],
                template=email_forgot_password_template,
            )
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Exception in Forgot Password, details:{e}")
            return HttpResponseBadRequest(
                "Sorry there was an error , please try again"
            )


class ForgotPasswordConfirmFormView(FormView):
    """
    Confirming user changing password
    """

    form_class = ForgotPasswordConfirmForm
    template_name = "account/forgot_password_confirm_form.html"
    success_url = reverse_lazy("account:user-login")

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        form.context = {"token": kwargs.get("token")}
        if form.is_valid():
            user = form.cleaned_data.get("user")
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class UserDashboardTemplateView(LoginRequiredMixin, TemplateView):
    """
    Shows the user dashboard
    """

    template_name = "account/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        return context
