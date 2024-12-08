from rest_framework import serializers
from room.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'quiz_subject', 'invitation_code']

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