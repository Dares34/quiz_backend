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
        url = reverse('auth')  # Замените на ваш URL-эндпоинт для авторизации
        data = {
            'login': 'wrong_email@example.com',  # Неверный email
            'password': 'wrong_password'          # Неверный пароль
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Invalid credentials'})