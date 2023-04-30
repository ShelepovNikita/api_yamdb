from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewsSet,
    ReviewViewSet,
    CommentReadViewSet
)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basemane='genre')
router.register('titles', TitleViewsSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='review'
                )
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentReadViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
