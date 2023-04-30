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
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentReadSerializer
)
from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModerOrAdminOrReadOnly)


class CategoryViewSet(viewsets.ModelViewSet):
    """API для модели категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_classes = LimitOffsetPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """API для модели жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_classes = LimitOffsetPagination
    filter_backends = (filters.SearchFilter)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewsSet(viewsets.ModelViewSet):
    """API для модели произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_classes = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """API для модели отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_classes = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrModerOrAdminOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)

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
