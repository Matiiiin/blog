from django import forms
from account.models import User, ContactUs
from django.shortcuts import get_object_or_404
import jwt
from blog.models import Post
from django.conf import settings


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


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


class UserPostCreateForm(forms.ModelForm):
    images = MultipleFileField()

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "hero_image",
            "images",
            "short_content",
            "main_content",
        ]
        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                    "required": True,
                }
            ),
            "hero_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
            "short_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Short content",
                    "rows": 7,
                    "cols": 30,
                    "required": True,
                }
            ),
            "main_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Main content",
                    "rows": 7,
                    "cols": 30,
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        images = cleaned_data.get("images")
        if len(images) != 3:
            self.add_error("images", "Please upload 3 images")
        return cleaned_data


class UserPostUpdateForm(forms.ModelForm):
    images = MultipleFileField(required=True)

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "hero_image",
            "images",
            "short_content",
            "main_content",
        ]
        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                    "required": True,
                }
            ),
            "hero_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
            "short_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Short content",
                    "rows": 7,
                    "cols": 30,
                    "required": True,
                }
            ),
            "main_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Main content",
                    "rows": 7,
                    "cols": 30,
                    "required": True,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        images = cleaned_data.get("images")
        title = cleaned_data.get("title")
        if (
            Post.objects.filter(title=title)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            self.add_error("title", "There is a post with this title")
        if len(images) != 3:
            self.add_error("images", "Please upload 3 images")
        return cleaned_data


class UserProfileUpdateForm(forms.Form):
    username = forms.CharField(
        required=False,
        max_length=255,
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new username",
            }
        ),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new email",
            }
        ),
    )
    first_name = forms.CharField(
        required=False,
        label="First name",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new first name",
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        label="Last name",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new last name",
            }
        ),
    )
    bio = forms.CharField(
        required=False,
        label="Bio",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new bio",
                "rows": 7,
                "cols": 30,
            }
        ),
    )
    image = forms.ImageField(
        required=False,
        label="Image",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        required=False,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop(
            "user", None
        )  # Handle cases where user might not exist
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        username = data.get("username")
        email = data.get("email")
        if (
            username != self.user.username
            and User.objects.filter(username=username).exists()
        ):
            self.add_error(
                "username", "There is a user with this username"
            )
        if User.objects.filter(email=email).exists():
            self.add_error("email", "There is a user with this email")
        return data
