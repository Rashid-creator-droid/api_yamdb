from django.core.validators import RegexValidator
from rest_framework import serializers, status
from rest_framework.response import Response
from reviews.models import ROLE_CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(
            regex='^[\w.@+-]+',
            message='Используйте допустимые символы в username'
        )])
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate(self, data):
        if 'email' in data:
            email = data['email']
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    f'Пользователь с email {email} уже существует!'
                )
        if 'username' in data:
            username = data['username']
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    f'Пользователь с username {username} уже существует!'
                )
            if username.lower() == 'me':
                raise serializers.ValidationError(
                    f'username {username} зарезервировано!'
                )
        return data


class MeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(
            regex='^[\w.@+-]+',
            message='Используйте допустимые символы в username'
        )])
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        required=False,
        read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(
            regex='^[\w.@+-]+',
            message='Используйте допустимые символы в username'
        )])
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        if 'email' in data:
            email = data.get('email')
        if 'username' in data:
            username = data.get('username')
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    f'Пользователь с email {email} уже существует!'
                )

            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    f'Пользователь с username {username} уже существует!'
                )
        if username.lower() == 'me':
            raise serializers.ValidationError(
                f'username {username} зарезервировано!'
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(
        max_length=150,
    )
    token = serializers.CharField(
        max_length=255,
        required=False,
        read_only=True
    )

    class Meta:
        fields = ('username', 'confirmation_code', 'token')
        model = User

    def validate(self, data):
        if 'username' in data:
            username = data['username']
        if 'confirmation_code' in data:
            confirmation_code = data.get('confirmation_code')
        if username == '':
            raise serializers.ValidationError(
                'Необходимо ввести username'
            )
        if confirmation_code == '':
            raise serializers.ValidationError(
                'Необходимо ввести присланный confirmation code'
            )
        return data
