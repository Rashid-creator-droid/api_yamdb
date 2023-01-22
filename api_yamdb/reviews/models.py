import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
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
