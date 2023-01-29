import datetime
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
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
    REQUIRED_FIELDS = ['email', 'bio', 'role']

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
 

now = datetime.now()


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
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        through='TitleGenre'
    )
    year = models.PositiveIntegerField(
        'Дата релиза',
        default=1895,
        validators=[MaxValueValidator(now.year), MinValueValidator(1895)],
    )
    description = models.TextField(
        'Описание произведения',
        max_length=1000,
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
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Жанры произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'Жанр произведения: "{self.title}" - {self.genre}'


class Review(models.Model):
    """Отзывы к произведениям."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(
        'Текст отзыва')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Комментарии к отзывам о произведениях."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(
        'Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
