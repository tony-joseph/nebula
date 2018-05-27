from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


class UserAPITestCase(TestCase):
    test_register_data = {
        'email': 'test@nebula.tonyj.me',
        'password': 'pass1234',
        'first_name': 'Test',
    }

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@nebula.tonyj.me',
            password='pass1234',
            first_name='User1',
        )
        self.user2 = User.objects.create_user(
            email='user2@nebula.tonyj.me',
            password='pass1234',
            first_name='User2',
        )
        self.user3 = User.objects.create_user(
            email='user3@nebula.tonyj.me',
            password='pass1234',
            first_name='User3',
        )

    def test_user_registration(self):
        client = APIClient()
        request = client.post(
            reverse('accounts:users-list'),
            self.test_register_data,
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        # Test login for new user
        request = client.post(
            reverse('accounts:get_auth_token'),
            {'username': self.test_register_data['email'], 'password': self.test_register_data['password']}
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        # Test user profile retrieve without auth token
        client = APIClient()
        request = client.get(
            reverse('accounts:users-detail', args=(self.user1.id,)),
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        # New client with auth token header
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key)

        # Test user profile retrieve
        request = client.get(
            reverse('accounts:users-detail', args=(self.user1.id,)),
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_edit_profile(self):
        user = User.objects.create_user(
            email='user-for-editing@nebula.tonyj.me',
            password='pass1234',
            first_name='Test'
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)

        # Test user profile edit
        data = {
            'first_name': 'New Test',
            'email': 'new-test@nebula.tonyj.me',
        }
        request = client.patch(
            reverse('accounts:users-detail', args=(user.id,)),
            data,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.json()['first_name'], data['first_name'])
        self.assertEqual(request.json()['email'], data['email'])

    def test_password_change(self):
        email = 'user-for-password-change@nebula.tonyj.me'
        old_password = 'pass1234'
        new_password = 'new' + old_password
        user = User.objects.create_user(
            email=email,
            password=old_password,
            first_name='Test'
        )
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)

        data = {'password': new_password}
        request = client.patch(
            reverse('accounts:users-detail', args=(user.id,)),
            data,
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Try authenticating with old password
        request = client.post(
            reverse('accounts:get_auth_token'),
            {'username': email, 'password': old_password}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        # Try authenticating with new password
        request = client.post(
            reverse('accounts:get_auth_token'),
            {'username': email, 'password': new_password}
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_users_endpoint(self):
        client = APIClient()
        request = client.get(
            reverse('accounts:users-list'),
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key)
        request = client.get(
            reverse('accounts:users-list'),
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        user_ids = map(
            lambda val: val['id'],
            request.json()['results'],
        )
        self.assertTrue(str(self.user1.id) in user_ids)
        self.assertTrue(str(self.user2.id) in user_ids)
        self.assertTrue(str(self.user3.id) in user_ids)
