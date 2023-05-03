import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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
    title = serializers.HiddenField(default='')

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Пользователь может оставить'
                        'только один отзыв на произведение. ',
            )
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра отзывов."""
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        model = Comment


class CommentWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для написания отзывов."""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        model = Comment
