from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterApiSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True)
    password_confirmation = serializers.CharField(
        required=True,
        write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'password',
            'password_confirmation',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким адресом электронной почты уже существует!!!')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True
    )

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                """
                User with this email 
                not found!Please resend
                with valid email"""
            )
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password', None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Not Found')

        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)

        return attrs


class RefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

        return data


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
