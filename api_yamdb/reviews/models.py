from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import RegexValidator
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер')
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, role, bio):
        if not username:
            raise ValueError('Необходимо ввести username')
        if not email:
            raise ValueError('Необходимо ввести email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            bio=bio
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role, bio):
        user = self.create_user(
            username,
            email,
            password=password,
            role=role,
            bio=bio
        )
        user.is_admin = True
        user.role = 'superuser'
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        db_index=True,
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex='^[\\w.@+-]+',
            message='ИСпользуйте допустимые символы в username'
        )],
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        db_index=True,
        unique=True,
    )

    first_name = models.CharField(
        ('First name'),
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        ('Last name'),
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        ('Bio'),
        blank=True,
    )

    role = models.CharField(
        ('User`s role'),
        max_length=20,
        default='user',
        choices=ROLE_CHOICES,
    )

    confirmation_code = models.CharField(
        ('Confirmation code'),
        max_length=150,
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now()
        td = timedelta(days=1)
        payload = self.pk
        token = jwt.encode(
            {
                'user_id': payload,
                'exp': int((dt + td).timestamp())
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return token

    class Meta:
        unique_together = ['username', 'email']
