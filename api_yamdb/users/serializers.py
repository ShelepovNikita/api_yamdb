from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации."""

    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    def validate_username(self, value):
        """Проверка на запрещенный username - me."""

        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(f"Недопустимо имя '{username}'")
        return value

    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserEditSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с личными данными поьзователя."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
