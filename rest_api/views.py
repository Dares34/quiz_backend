from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from room.models import Room, Participant
from quiz.models import Question, Quiz
from invitation.models import Invitation
from .serializers import UserSerializer, AuthSerializer, RoomSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['name']
        password = serializer.validated_data['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            return Response({'id': user.id, 'name': user.name, 'email': user.email})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'email': user.email,
                'name': user.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


