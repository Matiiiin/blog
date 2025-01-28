from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password' , 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True , 'style': {'input_type': 'password'}},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'details': 'Passwords do not match'})
        return data
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return super().create(validated_data)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'details': 'Invalid credentials'})
        else:
            attrs['user'] = user
        return attrs
class VerificationResendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get('email')
        user = get_object_or_404(User, email=email)
        if user.is_verified:
            raise serializers.ValidationError({'details': 'User is already verified'})
        attrs['user'] = user
        return attrs
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get('email')
        user = get_object_or_404(User, email=email)
        attrs['user'] = user
        return attrs
class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    current_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        user = get_object_or_404(User, email=email)
        if not user.check_password(current_password):
            raise serializers.ValidationError({'details': 'Current password is incorrect'})
        if new_password != new_password_confirm:
            raise serializers.ValidationError({'details': 'Passwords do not match'})
        attrs['user'] = user
        return attrs
class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(
                    {"details": msg}, code="authorization"
                )
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(
                {"details": msg}, code="authorization"
            )

        attrs["user"] = user
        return attrs