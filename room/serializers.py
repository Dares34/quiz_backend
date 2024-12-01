from rest_framework import serializers
from room.models import Room, Participant

class RoomSerializer(serializers.ModelSerializer):
    quizSubject = serializers.CharField(max_length=255)
    timer = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ['quizSubject', 'timer']
        extra_kwargs = {
            'quizSubject': {'required': True},
            'timer': {'required': True, 'min_value': 1},
        }

    # def create(self, validated_data):
    #     room = Room(**validated_data)
    #     room.save()
    #     return room