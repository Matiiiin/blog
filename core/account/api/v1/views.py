from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    CustomAuthTokenSerializer,
    VerificationResendSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordConfirmSerializer,
)
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from account.tasks import send_email
import logging
from account.utils import make_random_string
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class AuthGenericViewSet(viewsets.GenericViewSet):
    """
    a class for handling authentication
    """

    def get_serializer_class(self):
        serializers = {
            "register": RegisterSerializer,
            "login": LoginSerializer,
            "verification_resend": VerificationResendSerializer,
            "forgot_password": ForgotPasswordSerializer,
            "forgot_password_confirmation": ForgotPasswordConfirmSerializer,
        }
        return serializers.get(self.action)

    def get_permissions(self):
        if self.action in ["logout"]:
            return [IsAuthenticated()]
        return []

    @action(methods=["POST"], detail=False)
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        # send verification email
        token = RefreshToken.for_user(user)
        email_verification_template = render_to_string(
            "account/email_verification.html",
            {"token": token, "user": user},
        )
        send_email.delay(
            subject="Welcome to our blog",
            message="Thank you for registering",
            from_email="noreply@blog.com",
            recipient_list=[user.email],
            template=email_verification_template,
        )
        return Response(
            {"details": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(
            {"details": "User logged in successfully"},
            status=status.HTTP_200_OK,
        )

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        logout(request)
        return Response(
            {"details": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="verification-resend",
        url_name="verification-resend",
    )
    def verification_resend(self, request):
        serializer = VerificationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user)
        email_verification_template = render_to_string(
            "account/email_verification_resend.html",
            {"token": token, "user": user},
        )
        send_email.delay(
            subject="Account verification",
            from_email="noreply@blog.com",
            recipient_list=[user.email],
            template=email_verification_template,
        )
        return Response(
            {"details": "Verification email sent successfully"},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="forgot-password",
        url_name="forgot-password",
    )
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user)
        temp_password = make_random_string()
        user.set_password(temp_password)
        user.save()
        email_verification_template = render_to_string(
            "account/forgot_password.html",
            {
                "temp_password": temp_password,
                "user": user,
                "token": str(token),
            },
        )
        send_email.delay(
            subject="Reset password",
            from_email="noreply@blog.com",
            recipient_list=[user.email],
            template=email_verification_template,
        )
        return Response(
            {"details": "Temporary password sent successfully"},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="forgot-password-confirmation/(?P<token>[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+)",  # noqa
        url_name="forgot-password-confirmation",
    )
    def forgot_password_confirmation(self, request, token):
        serializer = ForgotPasswordConfirmSerializer(
            data=request.data, context={"token": token}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return Response(
            {"details": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )


class CustomAuthTokenLogin(ObtainAuthToken):
    """
    Login and generate a token for user in databsase
    """

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class CustomAuthTokenLogout(APIView):
    """
    Delete the token of user in database
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"details": "User logged out successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": f"Error logging out user {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
