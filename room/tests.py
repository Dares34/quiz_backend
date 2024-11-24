from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from room.models import Room, Participant

User = get_user_model()


class RoomTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(email='user1@example.com', name='User 1', password='testpass')
        self.user2 = User.objects.create_user(email='user2@example.com', name='User 2', password='testpass')

        # Create a room by user1
        self.room = Room.objects.create(quizSubject="Science", timer=60)
        self.participant1 = Participant.objects.create(userId=self.user1, roomId=self.room, score=0)

        # URL paths for room operations
        self.room_settings_url = reverse('room_settings', args=[self.room.id])
        self.start_quiz_url = reverse('start_quiz', args=[self.room.id])

    def test_create_room(self):
        # Test room creation by user1
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(reverse('create_room'), {
            'quizSubject': 'History',
            'timer': 30
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Room.objects.last().quizSubject, 'History')

    def test_update_room_settings_by_creator(self):
        # Test updating room settings by the room creator
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(self.room_settings_url, {
            'quizSubject': 'Math',
            'timer': 45
        })

        self.room.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.room.quizSubject, 'Math')
        self.assertEqual(self.room.timer, 45)

    def test_update_room_settings_by_non_creator(self):
        # Test that a non-creator cannot update room settings
        self.client.login(email='user2@example.com', password='testpass')
        response = self.client.post(self.room_settings_url, {
            'quizSubject': 'Geography',
            'timer': 20
        })

        self.assertEqual(response.status_code, 403)
        self.room.refresh_from_db()
        self.assertNotEqual(self.room.quizSubject, 'Geography')
        self.assertNotEqual(self.room.timer, 20)

    def test_start_quiz_by_creator(self):
        # Test that the room creator can start the quiz
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(self.start_quiz_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'Quiz started')

    def test_start_quiz_by_non_creator(self):
        # Test that a non-creator cannot start the quiz
        self.client.login(email='user2@example.com', password='testpass')
        response = self.client.post(self.start_quiz_url)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(response.json().get('status'), 'Quiz started')

    def test_room_creation_requires_login(self):
        # Test that login is required to create a room
        response = self.client.post(reverse('create_room'), {
            'quizSubject': 'Literature',
            'timer': 40
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
