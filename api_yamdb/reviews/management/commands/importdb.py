import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (
    User,
    Category,
    Genre,
    Title,
    Comment,
    Review,
    TitleGenre,
)

USERS = 'users.csv'
CATEGORY = 'category.csv'
GENRE = 'genre.csv'
TITLE = 'titles.csv'
GENRE_TITLE = 'genre_title.csv'
COMMENTS = 'comments.csv'
REVIEW = 'review.csv'


def get_reader(file):
    csv_path = os.path.join(settings.BASE_DIR, 'static/data/', file)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return reader


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            if User.objects.count() > 0:
                raise Exception('В базе уже есть данные users')
            csv_reader = get_reader(USERS)
            next(csv_reader, None)
            for row in csv_reader:
                obj, created = User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
            print(f'{USERS} успешно импортировалось!')

            if Category.objects.count() > 0:
                raise Exception('В базе уже есть данные Category')
            csv_reader = get_reader(CATEGORY)
            next(csv_reader, None)
            for row in csv_reader:
                obj, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            print(f'{CATEGORY} успешно импортировалось!')

            if Genre.objects.count() > 0:
                raise Exception('В базе уже есть данные Genre')
            csv_reader = get_reader(GENRE)
            next(csv_reader, None)
            for row in csv_reader:
                obj, created = Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            print(f'{GENRE} успешно импортировалось!')

            if Title.objects.count() > 0:
                raise Exception('В базе уже есть данные Title')
            csv_reader = get_reader(TITLE)
            next(csv_reader, None)
            for row in csv_reader:
                obj_category = get_object_or_404(Category, id=row[3])
                obj, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=obj_category,
                )
            print(f'{TITLE} успешно импортировалось!')

            if TitleGenre.objects.count() > 0:
                raise Exception('В базе уже есть данные TitleGenre')
            csv_reader = get_reader(GENRE_TITLE)
            next(csv_reader, None)
            for row in csv_reader:
                obj_genre = get_object_or_404(Genre, id=row[2])
                obj_title = get_object_or_404(Title, id=row[1])
                obj, created = TitleGenre.objects.get_or_create(
                    id=row[0],
                    genre=obj_genre,
                    title=obj_title,
                )
            print(f'{GENRE_TITLE} успешно импортировалось!')

            if Comment.objects.count() > 0:
                raise Exception('В базе уже есть данные Comment')
            csv_reader = get_reader(COMMENTS)
            next(csv_reader, None)
            for row in csv_reader:
                obj_review = get_object_or_404(Review, id=row[1])
                obj_user = get_object_or_404(User, id=row[3])
                obj, created = Comment.objects.get_or_create(
                    id=row[0],
                    review=obj_review,
                    text=row[2],
                    author=obj_user,
                    pub_date=row[4],
                )
            print(f'{COMMENTS} успешно импортировалось!')

            if Review.objects.count() > 0:
                raise Exception('В базе уже есть данные Review')
            csv_reader = get_reader('review.csv')
            next(csv_reader, None)
            for row in csv_reader:
                obj_title = get_object_or_404(Title, id=row[1])
                obj_user = get_object_or_404(User, id=row[3])
                obj, created = Review.objects.get_or_create(
                    id=row[0],
                    title=obj_title,
                    text=row[2],
                    author=obj_user,
                    score=row[4],
                    pub_date=row[5],
                )
            print(f'{REVIEW} успешно импортировалось!')
        except Exception as error:
            print(f'Ошибка импорта {error}')
