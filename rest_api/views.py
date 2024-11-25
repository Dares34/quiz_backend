from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from room.models import Room
import random
import string
from .serializers import RoomSerializer


class UsersViewSet(APIView):
    @extend_schema(
        request=UserSerializer,
        parameters=[
            OpenApiParameter(
                name='email',
                required=True
            ), OpenApiParameter(
                name='password',
                required=True
            )
        ],
        responses={201: UserSerializer, 403: "Неправильный логин или пароль"}
    )
    def get(self, request: HttpRequest):
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response('Wrong email or password', status=403)
        return Response({
            'name': user.name,
            'email': user.email,
            'role': user.role.name,  # или другой атрибут роли
        })


class CreateUserView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: "Ошибка валидации"}
    )
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
