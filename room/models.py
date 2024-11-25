from django.db import models
from user.models import User
import random
import string


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    quizSubject = models.CharField(max_length=255)
    timer = models.IntegerField()
    invitation_code = models.CharField(max_length=5, unique=True, blank=True, null=True)  # Код приглашения

    def save(self, *args, **kwargs):
        if not self.invitation_code:  # Генерация кода ТОЛЬКО при ПЕРВОМ СОХРАНЕНИИ
            self.invitation_code = self.generate_invitation_code()
        super(Room, self).save(*args, **kwargs)

    def generate_invitation_code(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(characters, k=5))
            if not Room.objects.filter(invitation_code=code).exists():
                return code

    def __str__(self):
        return f"Room {self.id} - {self.quizSubject}"


class Participant(models.Model):
    id = models.AutoField(primary_key=True)  # Инкрементируемый ID
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.userId.name
