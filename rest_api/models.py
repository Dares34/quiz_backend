from django.db import models


class Roles(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    is_admin = models.BooleanField(null=False, default=False)


class User(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    quizSubject = models.CharField(max_length=255)
    timer = models.IntegerField()

    def __str__(self):
        return self.name


class Participant(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.userId.name


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


class Invitation(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiverId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status
