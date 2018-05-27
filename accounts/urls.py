from django.urls import path, include
from rest_framework.authtoken import views as drf_views
from rest_framework.routers import DefaultRouter

from . import views as accouts_views


app_name = 'accounts'

router = DefaultRouter()
router.register('users', accouts_views.UserViewSet, base_name='users')

urlpatterns = [
    path('', include(router.urls)),

    path('get-auth-token/', drf_views.obtain_auth_token, name='get_auth_token'),
]
