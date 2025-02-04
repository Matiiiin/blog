from django import forms
from account.models import User , ContactUs
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username",
                "required": True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "required": True,
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = User.objects.filter(username=username).first()
        if user is None:
            raise forms.ValidationError("Invalid username")
        else:
            if not user.is_verified:
                raise forms.ValidationError("Account is not verified")
            if not user.check_password(password):
                raise forms.ValidationError("Invalid password")

        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm your password",
                "required": True,
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                    "required": True,
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your password",
                    "required": True,
                }
            ),
            "password_confirm": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Confirm your password",
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class EmailVerificationResendForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "required": True,
            }
        )
    )

    def clean(self):
        try:
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            user = User.objects.filter(email=email).first()
            if user is None:
                raise forms.ValidationError(
                    "Account associated to this email does not exist"
                )
            if user.is_verified:
                raise forms.ValidationError(
                    "Account is already verified"
                )
            cleaned_data["user"] = user
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(e)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "required": True,
            }
        )
    )

    def clean(self):
        try:
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            user = get_object_or_404(User, email=email)
            cleaned_data["user"] = user
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(e)


class ForgotPasswordConfirmForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "required": True,
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your new password",
                "required": True,
            }
        )
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm your password",
                "required": True,
            }
        )
    )

    def clean(self):
        try:
            cleaned_data = super().clean()
            token = self.context.get("token")
            user_id = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            ).get("user_id")
            current_password = cleaned_data.get("current_password")
            new_password = cleaned_data.get("new_password")
            new_password_confirm = cleaned_data.get(
                "new_password_confirm"
            )
            user = get_object_or_404(User, pk=user_id)

            if not user.check_password(current_password):
                raise forms.ValidationError(
                    "Current password is incorrect"
                )
            if new_password != new_password_confirm:
                raise forms.ValidationError("Passwords do not match")
            cleaned_data["user"] = user
            return cleaned_data
        except jwt.exceptions.InvalidSignatureError:
            raise forms.ValidationError("Invalid token")
        except jwt.exceptions.DecodeError:
            raise forms.ValidationError("Invalid token")
        except jwt.exceptions.ExpiredSignatureError:
            raise forms.ValidationError("Token has expired")
        except Exception as e:
            raise forms.ValidationError(e)

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email",
                    "required": True,
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Message",
                    "rows": 7,
                    "cols": 30,
                    "required": True,
                }
            ),
        }