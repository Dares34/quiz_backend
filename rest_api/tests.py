from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from room.models import Room, Participant
from quiz.models import Question, Quiz


# class AuthTestCase(APITestCase):
#     def setUp(self):
#         self.role = Roles.objects.create(name='User Role', is_admin=False)
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             name='Test User',
#             password='test_password',
#             role=self.role
#         )

#     def test_auth_invalid_credentials(self):
#         url = reverse('auth')
#         data = {
#             'name': 'wrong_email@example.com',
#             'password': 'wrong_password'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(response.data, {'error': 'Invalid credentials'})


class RoomViewSetTests(APITestCase):
    def test_create_room(self):
        data = {
            'quizSubject': 'Binary',
            'timer': 30
        }
        url = reverse('room-list')
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().quizSubject, 'Binary')
    
    def test_create_room_invalid_data(self):
        data = {
            'quizSubject': '',
            'timer': -10
        }
        url = reverse('room-list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Room.objects.count(), 0)

