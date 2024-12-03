import time
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


class IncrementWinsViewTestCase(TestCase):
    def setUp(self):
        """
        Создаем клиента и тестового пользователя для проверки.
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
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


class LoginTest(LiveServerTestCase):

    def setUp(self):
        """
        Настройка драйвера, создание пользователя и начальный URL.
        """
        self.user = get_user_model().objects.create_user(
            name='qwe123qwe123',
            email='qwe123qwe123@mail.ru',
            password='qwe123qwe123'
        )

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get('http://localhost:3000/login')

    def test_login_redirects_to_menu(self):
        """
        Тестируем успешный вход с редиректом на /menu.
        """
        driver = self.driver
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".log-submit"))
        )

        email_field = driver.find_element(By.ID, "login")
        password_field = driver.find_element(By.ID, "password")

        email_field.send_keys('qwe123qwe123@mail.ru')
        password_field.send_keys('qwe123qwe123')
        password_field.send_keys(Keys.RETURN)
        login_button.click()
        time.sleep(5)
        self.assertEqual(driver.current_url, 'http://localhost:3000' + "/menu")

    def tearDown(self):
        """
        Закрытие драйвера после выполнения теста.
        """
        self.driver.quit()
