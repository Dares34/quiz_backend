from rest_framework import viewsets
from .models import User, Room, Participant, Question, Quiz, Invitation
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
