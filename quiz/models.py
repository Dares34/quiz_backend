from django.db import models
# from room.models import Room

class Question(models.Model):
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="questions")
    quiz_subject = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Question {self.id} ({self.quiz_subject})"

# class Quiz(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="quizzes", blank=True, null=True)
#     question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="quiz", blank=True, null=True)

#     def __str__(self):
#         return f"Quiz for Room {self.room.id} with {self.questions.count()} questions"

