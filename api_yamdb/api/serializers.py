import datetime as dt

from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        model = Title

    def get_rating(self, obj):
        if obj.reviews.exists():
            return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleNewSerializer(serializers.ModelSerializer):
    """Сериализатор для новых произведений."""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше текущего')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(validators=[
        MinValueValidator(limit_value=1,
                          message='Минимальное значение - 1'),
        MaxValueValidator(limit_value=10,
                          message='Максимальное значение - 10')
    ])

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title_id=title.id,
                                     author=author).exists():
                raise ValidationError('Вы можете оставить только 1 отзыв')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра отзывов."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
