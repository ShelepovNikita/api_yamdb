from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, get_token, sign_up


router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token'),
]
