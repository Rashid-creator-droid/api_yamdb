from django.db import models
from django.core.validators import MaxValueValidator
import datetime

now = datetime.datetime.now()


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
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        null=True,
    )
    year = models.PositiveIntegerField(
        'Дата релиза',
        default=1895,
        validators=[MaxValueValidator(now.year)],
    )
    description = models.TextField('Описание произведения', max_length=1000)
    user_rating = 1

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
