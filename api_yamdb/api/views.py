from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentReadSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_classes = LimitOffsetPagination
    # дописать пермишен кому доступны категории
    # дописать filter_backends и serch_fields


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_classes = LimitOffsetPagination
    # дописать пермишен кому доступны категории
    # дописать filter_backends и serch_fields


class TitleViewsSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_classes = LimitOffsetPagination
    # дописать пермишен кому доступны категории
    # фильтрация по категории и жанру


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_classes = LimitOffsetPagination
    # дописать пермишен кому доступны категории
    # тут будет perform create
    # а тут get_queryset


class CommentReadViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    pagination_classes = LimitOffsetPagination
    # дописать пермишен кому доступны категории
    # тут будет perform create
    # а тут get_queryset
