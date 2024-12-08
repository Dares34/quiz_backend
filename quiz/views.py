from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

class CreateQuizQuestionsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer

    @extend_schema(
        tags=["question"],
        summary="Добавить вопрос",
        responses={200: QuestionSerializer}
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response({
                'success': 'вопросы для темы созданы',
                'quiz_subject': question.quiz_subject,
                'data': question.data,
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# class CreateQuizView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]
#     serializer_class = QuizCreateSerializer

#     @extend_schema(
#         tags=["quiz"],
#         summary="Создать квиз",
#         responses={200: QuizCreateSerializer(many=True)}
#     )
#     def post(self, request):
#         serializer = QuizCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             quiz = serializer.save()
#             return Response({
#                 'success': 'Квиз создан',
#                 'quiz_id': quiz.id,
#                 'room_id': quiz.room.id,
#                 'question_id': quiz.question.id
#             }, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)