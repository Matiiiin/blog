from django.views.generic import (
    TemplateView,
    FormView,
    CreateView,
    View,
    ListView,
    UpdateView,
    DeleteView,
)
from account.models import User, ContactUs
from blog.models import Comment, CommentReply, Post, Image
from .forms import (
    LoginForm,
    UserRegistrationForm,
    EmailVerificationResendForm,
    ForgotPasswordForm,
    ForgotPasswordConfirmForm,
    ContactUsForm,
    UserPostUpdateForm,
    UserPostCreateForm,
    UserProfileUpdateForm,
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
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


# Create your views here.
logger = logging.getLogger(__name__)


class HomePageTemplateView(TemplateView):
    """
    Shows index view of website
    """

    template_name = "index.html"

    @method_decorator(cache_page(60 * 10, key_prefix="homepage"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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
            current_site = get_current_site(self.request)
            email_verification_template = render_to_string(
                "account/email_verification.html",
                {
                    "user": user,
                    "token": token,
                    "current_site": current_site.domain,
                },
            )
            send_email.delay(
                subject="Welcome to our blog",
                message="Thank you for registering",
                from_email="noreply@blog.com",
                recipient_list=[user.email],
                template=email_verification_template,
            )
            messages.success(
                self.request,
                "Verification email has been sent , please check your email",
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
            current_site = get_current_site(self.request)
            email_verification_template = render_to_string(
                "account/email_verification_resend.html",
                {
                    "user": user,
                    "token": token,
                    "current_site": current_site.domain,
                },
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
            current_site = get_current_site(self.request)
            email_forgot_password_template = render_to_string(
                "account/forgot_password.html",
                {
                    "user": user,
                    "temp_password": temp_password,
                    "token": str(token),
                    "current_site": current_site.domain,
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

    template_name = "account/dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context["profile"] = profile
        context["latest_comments"] = profile.comments.order_by(
            "-created_at"
        )[:5]
        context["latest_replies"] = profile.replies.order_by(
            "-created_at"
        )[:5]
        return context


class ContactUsCreateView(CreateView):
    """
    Shows the contact us form
    """

    model = ContactUs
    form_class = ContactUsForm
    template_name = "account/contact_us.html"
    success_url = reverse_lazy("homepage")

    @method_decorator(cache_page(60 * 10, key_prefix="contact_us"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AboutUsTemplateView(TemplateView):
    """
    Shows the about us page
    """

    template_name = "account/about_us.html"

    @method_decorator(cache_page(60 * 10, key_prefix="about-us"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = [
            "about_us/hero_1.jpg",
            "about_us/hero_2.jpg",
            "about_us/hero_5.jpg",
            "about_us/img_7_sq.jpg",
        ]
        context["images"] = [
            settings.MEDIA_URL + image for image in images
        ]
        context["team"] = User.objects.get(
            email="matinnjt2000@gmail.com"
        ).profile
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    template_name = "account/dashboard/user_posts.html"
    paginate_by = 7
    context_object_name = "posts"

    def get_queryset(self):
        return self.request.user.profile.posts.order_by(
            "-created_at"
        ).all()


class UserPostCreateView(LoginRequiredMixin, CreateView):
    template_name = "account/dashboard/user_post_create.html"
    form_class = UserPostCreateForm
    success_url = reverse_lazy("account:user-posts")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.profile
        post.save()
        images = self.request.FILES.getlist("images")
        for image in images:
            created_image = Image(image=image)
            created_image.save()
            post.images.add(created_image)
        return HttpResponseRedirect(self.success_url)


class UserPostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "account/dashboard/user_post_update.html"
    form_class = UserPostUpdateForm
    model = Post
    success_url = reverse_lazy("account:user-posts")
    slug_field = "slug"
    context_object_name = "post"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        images = self.request.FILES.getlist("images")
        if images:
            post.images.clear()
            for image in images:
                created_image = Image(image=image)
                created_image.save()
                post.images.add(created_image)
        return HttpResponseRedirect(self.success_url)


class UserPostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("account:user-posts")
    slug_field = "slug"
    context_object_name = "post"
    template_name = "account/dashboard/user_post_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("account:user-posts")
        return context


class UserProfileUpdateView(FormView):
    template_name = "account/dashboard/user_settings.html"
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy("account:user-dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user_fields = ["email", "username"]
        for field in user_fields:
            if form.cleaned_data.get(field):
                setattr(user, field, form.cleaned_data.get(field))
        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data.get("password"))
        user.save()
        profile_fields = ["first_name", "last_name", "bio", "image"]
        for field in profile_fields:
            if form.cleaned_data.get(field):
                setattr(
                    user.profile, field, form.cleaned_data.get(field)
                )
        if form.cleaned_data.get("image") is not None:
            user.profile.image = form.cleaned_data.get(
                "image", user.profile.image
            )
        user.profile.save()
        return super().form_valid(form)
