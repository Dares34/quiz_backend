from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from room.models import Room, Participant
from quiz.models import Question, Quiz
from invitation.models import Invitation
from .serializers import UserSerializer, AuthSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']
        password = serializer.validated_data['password']
        user = authenticate(username=login, password=password)
        if user is not None:
            return Response({'id': user.id, 'username': user.username, 'email': user.email})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
