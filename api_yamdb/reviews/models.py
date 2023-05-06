from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api.validators import validate_year
from reviews.constains import NAME_LENGTH, SLUG_LENGTH
from users.models import User


class Сharacteristic(models.Model):
    name = models.CharField(max_length=NAME_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(max_length=SLUG_LENGTH,
                            unique=True, null=False,
                            verbose_name='Человекопонятный URL')

    class Meta:
        abstract = True


class Category(Сharacteristic):

    class Meta:
        ordering = ['name']
        verbose_name = "Категория"


class Genre(Сharacteristic):

    class Meta:
        ordering = ['name']
        verbose_name = "Жанр"


class Title(models.Model):
    name = models.CharField(max_length=NAME_LENGTH,
                            verbose_name='Название')
    year = models.IntegerField(verbose_name='Год',
                               validators=[validate_year])
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        null=True, verbose_name='Категория')

    class Meta:
        ordering = ['year']
        verbose_name = "Произведение"


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва')
    score = models.IntegerField(verbose_name='Оценка', validators=[
        MinValueValidator(limit_value=1,
                          message='Минимальное значение - 1'),
        MaxValueValidator(limit_value=10,
                          message='Максимальное значение - 10')
    ])
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        verbose_name = "Отзыв"


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ['pub_date']
        verbose_name = "Комментарий"
