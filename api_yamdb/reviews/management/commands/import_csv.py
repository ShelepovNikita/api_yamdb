import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User)


class Command(BaseCommand):
    help = 'Импорт данных в таблицы из csv файлов'

    def handle(self, *args, **kwargs):
        self.users_upload()
        self.categories_upload()
        self.genres_upload()
        self.titles_upload()
        self.reviews_upload()
        self.comments_upload()
        self.genres_titles()

    def users_upload(self):
        users_data = Path(Path.cwd(), "static", "data", "users.csv")
        with open(users_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_users = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    user = (User(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    ))
                    list_users.append(user)
        try:
            User.objects.bulk_create(list_users)
            print('Добавлены записи в таблицу Users')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Users: {error}')

    def categories_upload(self):
        categories_data = Path(Path.cwd(), "static", "data", "category.csv")
        with open(categories_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_categories = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    category = (Category(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ))
                    list_categories.append(category)
        try:
            Category.objects.bulk_create(list_categories)
            print('Добавлены записи в таблицу Categories')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Categories: {error}')

    def genres_upload(self):
        genres_data = Path(Path.cwd(), "static", "data", "genre.csv")
        with open(genres_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_genres = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    genre = (Genre(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ))
                    list_genres.append(genre)
        try:
            Category.objects.bulk_create(list_genres)
            print('Добавлены записи в таблицу Genres')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Genres: {error}')

    def titles_upload(self):
        titles_data = Path(Path.cwd(), "static", "data", "titles.csv")
        with open(titles_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_titles = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    title = (Title(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category_id=row[3]
                    ))
                    list_titles.append(title)
        try:
            Title.objects.bulk_create(list_titles)
            print('Добавлены записи в таблицу Titles')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Titles: {error}')

    def reviews_upload(self):
        reviews_data = Path(Path.cwd(), "static", "data", "review.csv")
        with open(reviews_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_reviews = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    review = (Review(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        score=row[4],
                        pub_date=row[4],
                    ))
                    list_reviews.append(review)
        try:
            Review.objects.bulk_create(list_reviews)
            print('Добавлены записи в таблицу Review')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Review: {error}')

    def comments_upload(self):
        comments_data = Path(Path.cwd(), "static", "data", "comments.csv")
        with open(comments_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            list_comments = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    comment = (Comment(
                        id=row[0],
                        review_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        pub_date=row[4],
                    ))
                    list_comments.append(comment)
        try:
            Comment.objects.bulk_create(list_comments)
            print('Добавлены записи в таблицу Comments')
        except Exception as error:
            print(f'Ошибка при добавлении в таблицу Comments: {error}')

    def genres_titles(self):
        genres_titles_data = Path(Path.cwd(),
                                  "static", "data", "genre_title.csv")
        with open(genres_titles_data, encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            # list_genres_titles = []
            for count, row in enumerate(file_reader):
                if count != 0:
                    title = Title.objects.get(id=row[1])
                    genre = Genre.objects.get(id=row[2])
                    title.genre.add(genre)
