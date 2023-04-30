from rest_framework import serializers
from django.db.models import Avg

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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Title

    def get_rating(self, obj):
        rating = obj.review.aggregate(raiting=Avg('score'))
        return rating.get('score__avg')


class TitleNewSerializer(serializers.ModelSerializer):
    """Сериализатор для новых произведений."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        read_only=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


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
