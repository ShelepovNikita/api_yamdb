from rest_framework.routers import SimpleRouter
from django.urls import include, path

from users.views import (
    UsersViewSet,
    get_token,
    sign_up
)
from api_yamdb.settings import VERSION_API


router_v1 = SimpleRouter()
router_v1.register(r'users', UsersViewSet)
urlpatterns = [
    path(f'{VERSION_API}', include(router_v1.urls)),
    path(f'{VERSION_API}auth/signup/', sign_up, name='sign_up'),
    path(f'{VERSION_API}auth/token/', get_token, name='get_token'),
]
