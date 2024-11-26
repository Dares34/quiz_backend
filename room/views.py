from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer
# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(ownere=self.request.user)

    def add_participant(self, request, pk = None):
        room = self.get_object()
        user = request.user
        if user not in room.participants.all():
            room.participnats.addig(user)
            return Response({'status': 'User added to room'}, status=status.HTTP_200_OK)
        return Response({'status': 'User already in room'}, status= status.HTTP_400_BAD_REQUEST)

    def remove_participant(self, request, pk = None):
        room = self.get_object()
        user = request.user
        if user in room.participants.all():
            room.participants.remove(user)
            return Response({'status':'User removed from room'}, status = status.HTTP_200_OK)
        return Response({'status': 'User not in room'}, status=status.HTTP_400_BAD_REQUEST)
    