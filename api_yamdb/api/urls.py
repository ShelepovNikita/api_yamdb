from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewsSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewsSet, basename='title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='review'
                   )
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
