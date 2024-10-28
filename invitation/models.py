from django.db import models
from user.models import User
from room.models import Room


class Invitation(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    roomId = models.ForeignKey(Room, on_delete=models.CASCADE)
    senderId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiverId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status
