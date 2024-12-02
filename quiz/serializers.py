from rest_framework import serializers
from .models import Question, Quiz
from room.models import Room
from room.serializers import RoomSerializer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'data', 'name']

class QuizSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'room', 'questions']

    def create(self, validated_data):
        room_data = validated_data.pop('room')
        questions_data = validated_data.pop('questions')

        room = Room.objects.create(**room_data)
        quiz = Quiz.objects.create(room=room)

        for question_data in questions_data:
            question = Question.objects.create(**question_data)
            quiz.questions.add(question)

        return quiz
