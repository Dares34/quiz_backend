from rest_framework import serializers
from user.models import User
from room.models import Room, Participant

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['quizSubject', 'timer']
        extra_kwargs = {
            'quizSubject': {'required': True},
            'timer': {'required': True, 'min_value': 1},
        }