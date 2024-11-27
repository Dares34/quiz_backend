from rest_framework import serializers
from room.models import Room
from quiz.models import Question, Quiz

class RoomSerializer(serializers.ModelSerializer):
    quiz_subject = serializers.CharField()
    timer = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ['quiz_subject', 'timer']
