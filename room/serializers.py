from rest_framework import serializers
from room.models import Room
from quiz.serializers import QuestionSerializer

class RoomSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True, read_only=True
    )
    class Meta:
        model = Room
        fields = ['id', 'quiz_subject', 'invitation_code', 'questions', 'timer']

class AddParticipantSerializer(serializers.Serializer):
    participant_id = serializers.CharField(max_length=255)
    participant_name = serializers.CharField(max_length=255)

class IncrementScoreSerializer(serializers.Serializer):
    participant_id = serializers.CharField(max_length=255)
    score = serializers.IntegerField(default=1, min_value=1)

class RoomStatusSerializer(serializers.Serializer):
    participants = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        default = [],
        help_text = "Список участников комнатыб каждый из которых представлен в виде словаря с ID и именем"
    )
    scores = serializers.DictField(
        child = serializers.IntegerField(),
        default = {},
        help_text = "Список очков участников, где ключ - Id участника, со значением - количество очков",
    )
    quiz_subject = serializers.CharField(
        max_length = 255, 
        help_text = "Предмет квиза в комнате",
    )
    invitation_code = serializers.CharField(
        max_length = 5,
        help_text = "Код комнаты",
    )