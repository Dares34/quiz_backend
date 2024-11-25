from rest_framework import serializers
from user.models import User
from room.models import Room, Participant
from quiz.models import Question, Quiz


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()


class RoomSerializer(serializers.ModelSerializer):
    quiz_subject = serializers.CharField()
    timer = serializers.IntegerField()

    class Meta:
        model = Room
        fields = ['quiz_subject', 'timer']
