from django.db import models


class Question(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    text = models.CharField(max_length=255)
    correctAnswer = models.CharField(max_length=255)
    dificulty = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    subjectArea = models.CharField(max_length=255)
    questions = models.CharField(max_length=255)
    currentQuestionIndex = models.ForeignKey(Question, on_delete=models.PROTECT)
    timeLimit = models.IntegerField()

    def __str__(self):
        return self.subjectArea
