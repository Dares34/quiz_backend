from rest_framework import serializers
from user.models import User
from room.models import Room, Participant
from quiz.models import Question, Quiz

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'role']  # Укажите необходимые поля

    def create(self, validated_data):
        password = validated_data.pop('password')  # Извлекаем пароль
        user = User(**validated_data)  # Создаем пользователя
        user.set_password(password)  # Устанавливаем зашифрованный пароль
        user.save()  # Сохраняем пользователя
        return user


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['quizSubject', 'timer']