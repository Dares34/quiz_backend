from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User, Roles


class AuthTestCase(APITestCase):
    def setUp(self):
        self.role = Roles.objects.create(name='User Role', is_admin=False)
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='test_password',
            role=self.role
        )

    def test_auth_invalid_credentials(self):
        url = reverse('auth')
        data = {
            'name': 'wrong_email@example.com',
            'password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Invalid credentials'})

    def test_auth_success(self):
        url = reverse('auth')
        data = {
            'name': 'test@example.com',
            'password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
