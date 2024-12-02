from django.db import models
from room.models import Room

class Question(models.Model):
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="questions")
    name = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return f"Question {self.id} in Room {self.room.name}"

class Quiz(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="quizzes")
    questions = models.ManyToManyField(Question, related_name="quizzes")

    def __str__(self):
        return f"Quiz for Room {self.room.id} with {self.questions.count()} questions"
