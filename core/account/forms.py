from django import forms
from account.models import User
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'required': True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'required': True,
            }
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise forms.ValidationError('Invalid username')
        if not user.check_password(password):
            raise forms.ValidationError('Invalid password')
        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True,
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'required': True,
            }),
            'password_confirm': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
                'required': True,
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
class EmailVerificationResendForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True,
            }
        )
    )
    def clean(self):
        try:
            cleaned_data = super().clean()
            email = cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user is None:
                raise forms.ValidationError('Account associated to this email does not exist')
            if user.is_verified:
                raise forms.ValidationError('Account is already verified')
            cleaned_data['user'] = user
            return cleaned_data
        except Exception as e:
            raise forms.ValidationError(e)