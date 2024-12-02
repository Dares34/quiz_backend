from rest_framework import serializers
from .models import Question, Quiz
from room.models import Room
from room.serializers import RoomSerializer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'data', 'name']

class QuizCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)
    question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'room_id', 'question_id']

    def create(self, validated_data):
        room_id = validated_data.pop('room_id')
        question_id = validated_data.pop('question_id')

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError({'room_id': 'Комната не найдена.'})

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise serializers.ValidationError({'question_id': 'Вопрос не найден.'})

        quiz = Quiz.objects.create(room=room, question=question)

        return quiz
