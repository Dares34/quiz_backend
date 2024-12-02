from django.db import models
from user.models import User
import random
import string
# from rest_framework.views import APIView


class Room(models.Model):
    quiz_subject = models.CharField(max_length=255)
    invitation_code = models.CharField(max_length=5, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f"Room {self.id} - {self.quizSubject}"

