from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from room.models import Room, Participant
from invitation.models import Invitation

User = get_user_model()


class InvitationTests(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(email='user1@example.com', name='User 1', password='testpass')
        self.user2 = User.objects.create_user(email='user2@example.com', name='User 2', password='testpass')
        self.user3 = User.objects.create_user(email='user3@example.com', name='User 3', password='testpass')
        self.user4 = User.objects.create_user(email='user4@example.com', name='User 4', password='testpass')
        self.user5 = User.objects.create_user(email='user5@example.com', name='User 5', password='testpass')

        # Создание комнаты и юезра1 как зшедшего-владельца
        self.room = Room.objects.create(quizSubject="General Knowledge", timer=30)
        self.participant1 = Participant.objects.create(userId=self.user1, roomId=self.room, score=0)

        self.invite_url = reverse('invite_user', args=[self.room.id])

    def test_invite_user_success(self):
        # Приглашение юзера2 в комнату
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(self.invite_url, {'invited_user_id': self.user2.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Приглашение отправлено', response.json().get('success'))
        self.assertTrue(Invitation.objects.filter(room=self.room, invited_user=self.user2).exists())

    def test_invite_user_room_full(self):
        # Заполнение комнаты полностью
        Participant.objects.create(userId=self.user2, roomId=self.room, score=0)
        Participant.objects.create(userId=self.user3, roomId=self.room, score=0)
        Participant.objects.create(userId=self.user4, roomId=self.room, score=0)

        # Пробуем пригласить юзера5, когда комната заполнена
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(self.invite_url, {'invited_user_id': self.user5.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Комната уже заполнена', response.json().get('error'))
        self.assertFalse(Invitation.objects.filter(room=self.room, invited_user=self.user5).exists())

    def test_invite_nonexistent_user(self):
        # Тест приглашения несуществуещего пользователя
        self.client.login(email='user1@example.com', password='testpass')
        response = self.client.post(self.invite_url, {'invited_user_id': 999})

        self.assertEqual(response.status_code, 404)

    def test_invite_user_not_logged_in(self):
        # Приглашение пользователя без логина
        response = self.client.post(self.invite_url, {'invited_user_id': self.user2.id})
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    def test_invite_user_already_invited(self):
        # Попытка дважды пригласить юзера2
        self.client.login(email='user1@example.com', password='testpass')
        Invitation.objects.create(room=self.room, invited_user=self.user2)
        response = self.client.post(self.invite_url, {'invited_user_id': self.user2.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Приглашение отправлено', response.json().get('success'))
        self.assertEqual(Invitation.objects.filter(room=self.room, invited_user=self.user2).count(), 1)
