from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


class AuthTestCase(TestCase):
    test_user_email = 'test@nebula.tonyj.me'
    test_user_password = 'pass1234'

    def setUp(self):
        user = User.objects.create_user(first_name='test', email=self.test_user_email, password=self.test_user_password)
        self.user = user

    def test_token_auth_success(self):
        client = APIClient()
        request = client.post(
            reverse('accounts:get_auth_token'),
            {'username': self.test_user_email, 'password': self.test_user_password}
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.json()['token'], self.user.auth_token.key)

    def test_token_auth_invalid_credentials(self):
        client = APIClient()
        request = client.post(
            reverse('accounts:get_auth_token'),
            {'username': self.test_user_email, 'password': self.test_user_password + 'invalid'}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
