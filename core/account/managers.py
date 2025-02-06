from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_kwargs):
        if not username:
            raise ValueError("username must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, **extra_kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, email, password, **extra_kwargs
    ):
        extra_kwargs.setdefault("is_superuser", True)
        extra_kwargs.setdefault("is_staff", True)
        extra_kwargs.setdefault("is_active", True)
        extra_kwargs.setdefault("is_verified", True)

        if extra_kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser")

        if extra_kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        return self.create_user(
            username, email, password, **extra_kwargs
        )
