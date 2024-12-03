from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from django.urls import reverse


class IncrementWinsViewTestCase(TestCase):
    def setUp(self):
        """
        Создаем клиента и тестового пользователя для проверки.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            password="password123",
        )
        # Добавляем начальное количество побед
        self.user.wins = 5
        self.user.save()
        self.url = self.invite_url = reverse('increment-wins')

    def test_increment_wins_success(self):
        """
        Тестируем успешное увеличение побед.
        """
        response = self.client.post(self.url, {"email": self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.wins, 6)  # Увеличение на 1
        self.assertEqual(response.json(), {"email": self.user.email, "wins": 6})

    def test_increment_wins_user_not_found(self):
        """
        Тестируем случай, когда пользователь не найден.
        """
        response = self.client.post(self.url, {"email": "notfound@example.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Пользователь не найден"})

    def test_increment_wins_missing_email(self):
        """
        Тестируем случай, когда email не передан в запросе.
        """
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"detail": "Email не предоставлен"})

