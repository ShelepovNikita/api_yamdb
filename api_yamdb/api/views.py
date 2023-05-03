from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleNewSerializer,
    ReviewSerializer,
    CommentReadSerializer,
    CommentWriteSerializer
)
from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModerOrAdminOrReadOnly)
from api.viewsets import CreateListDestroyViewSet


class CategoryViewSet(CreateListDestroyViewSet):
    """API для модели категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """API для модели жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class TitleViewsSet(viewsets.ModelViewSet):
    """API для модели произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleNewSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """API для модели отзывов."""
    serializer_class = ReviewSerializer
    pagination_classes = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModerOrAdminOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = Title.objects.get(pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.filter(title=title_id)
        return review_queryset


class CommentReadViewSet(viewsets.ModelViewSet):
    """API для модели комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentReadSerializer
    pagination_classes = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModerOrAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CommentWriteSerializer
        return CommentReadSerializer
