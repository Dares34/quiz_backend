from rest_framework import serializers
from .models import User, Room, Participant, Question, Quiz, Invitation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']
