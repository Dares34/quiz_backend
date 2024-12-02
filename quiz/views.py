from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Question, Quiz
from .serializers import RoomSerializer, QuizSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

class CreateQuizView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    @extend_schema(
        tags=["room"],
        summary="Создать команту",
        responses={200: RoomSerializer(many=True)}
    )
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            quiz = serializer.save()
            return Response({'success': 'Квиз создан', 'quiz': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
