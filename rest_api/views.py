from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from room.models import Room
import random
import string
from .serializers import RoomSerializer


#API создание комнаты
class CreateRoomView(APIView):
    @extend_schema(
        request=RoomSerializer,
        responses={201: "Room created successfully", 400: "Validation error"},
        examples=[
            OpenApiExample(
                name="Create Room Example",
                value={
                    "quiz_subject": "Science",
                    "timer": 30
                },
                description="Пример данных для создания комнаты"
            )
        ]
    )
    def post(self, request):
        quiz_subject = request.data.get('quiz_subject')
        timer = request.data.get('timer')

        if not quiz_subject or not isinstance(timer, int):
            return Response({'error': 'Invalid quiz_subject or timer'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерация кода приглашения
        def generate_invitation_code():
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        try:
            invitation_code = generate_invitation_code()
            room = Room.objects.create(
                quizSubject=quiz_subject,
                timer=timer,
                invitation_code=invitation_code
            )
            return Response({
                'message': 'Room created successfully',
                'invitation_code': invitation_code
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
