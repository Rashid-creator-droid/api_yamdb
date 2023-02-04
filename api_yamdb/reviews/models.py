from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from api.usermanager import UserManager

NOW = datetime.now()
ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер'),
)


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        db_index=True,
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+',
            message='ИСпользуйте допустимые символы в username',
        )],
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        db_index=True,
        unique=True,
    )

    first_name = models.CharField(
        'First name',
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        'Last name',
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        'Bio',
        blank=True,
    )

    role = models.CharField(
        'User`s role',
        max_length=20,
        default='user',
        choices=ROLE_CHOICES,
    )

    confirmation_code = models.CharField(
        'Confirmation code',
        max_length=150,
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'bio', 'role']

    class Meta:
        unique_together = ['username', 'email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_administrator(self):
        return self.role == 'admin'

    @property
    def is_superuser(self):
        return self.role == 'superuser'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = NOW
        td = timedelta(days=1)
        payload = self.pk
        token = jwt.encode(
            {
                'user_id': payload,
                'exp': int((dt + td).timestamp()),
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return token


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Ссылка', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Произведение', max_length=256)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='TitleGenre',
    )
    year = models.PositiveIntegerField(
        'Дата релиза',
        default=NOW,
        validators=[MaxValueValidator(NOW.year)],
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Жанры произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'Произведение:"{self.title}". Жанр:{self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Допустимые значние 1-10'),
            MaxValueValidator(10, message='Допустимые значние 1-10'),

        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
