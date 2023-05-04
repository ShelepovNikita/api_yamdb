import csv

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.models import User
from api_yamdb.settings import BASE_DIR


MODEL_CSV_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

CSV_PATH = f'{BASE_DIR}/static/data/'


class Command(BaseCommand):
    help = 'Импорт данных в таблицы из csv файлов'

    def handle(self, *args, **kwargs):
        self.models_upload()
        try:
            self.genres_titles()
            print('Таблица genre_titles импортирована')
        except Exception as error:
            print(f'Ошибки при импортировании таблицы genre_titles: {error}')

    def models_upload(self):
        for model, csv_file in MODEL_CSV_DICT.items():
            with open(str(CSV_PATH) + csv_file, encoding='utf-8') as r_file:
                reader = csv.DictReader(r_file)
                csv_data = []
                for row in reader:
                    if row.get('category') is not None:
                        row['category'] = Category.objects.get(
                            id=row['category'])
                    if row.get('author') is not None:
                        row['author'] = User.objects.get(
                            id=row['author'])
                    csv_data.append(model(**row))
                try:
                    model.objects.bulk_create(csv_data)
                    print(f'Добавлены записи в таблицу {model.__name__}')
                except IntegrityError:
                    print(f'Данные модели {model.__name__} уже импортированы')

    def genres_titles(self):
        with open(str(CSV_PATH) + 'genre_title.csv',
                  encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for count, row in enumerate(file_reader):
                if count != 0:
                    title = Title.objects.get(id=row[1])
                    genre = Genre.objects.get(id=row[2])
                    title.genre.add(genre)
