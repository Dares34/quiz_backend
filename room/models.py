from django.db import models
from user.models import User


class Room(models.Model):
    # id = models.IntegerField(primary_key=True, serialize=True)
    # name = models.CharField(max_length=255)
    quizSubject = models.CharField(max_length=255)
    timer = models.IntegerField()

    # def __str__(self):
    #     return self.


class Participant(models.Model):
    # id = models.IntegerField(primary_key=True, serialize=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.userId.name
