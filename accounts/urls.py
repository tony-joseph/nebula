from django.urls import path
from rest_framework.authtoken import views as drf_views

app_name = 'accounts'

urlpatterns = [
    path('get-auth-token/', drf_views.obtain_auth_token, name='get_auth_token'),
]
