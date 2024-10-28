from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']


class AuthSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
