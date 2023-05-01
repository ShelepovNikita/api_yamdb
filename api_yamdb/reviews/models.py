
from django.contrib.auth.models import AbstractUser
from django.db import models


# Все модели черновые, будут обрастать данными в процессе разработки.
# Не забывайте делать миграции.

# Модель юзер построена через абстрактюзер по подсказке под заданием яндекса.
class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    bio = models.TextField(blank=True,)
    role = models.CharField(
        max_length=50, choices=ROLES, blank=True, default='user')


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, null=False)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True, null=False)


# Здесь хитро сделана таблица, связывающая произведения и жанры.
# Таблица genre_title из схемы которую я скидывал в телеграмме
# создается автоматически с помощью поля ManyToManyField
class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField(null=True)
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name='genres')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='categories',
        null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)