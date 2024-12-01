from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'data_joined', 'is_staff']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    # class Meta:
    #     model = User
    #     fields = ['id', 'name', 'email','password']
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # print(email, password)

        user = authenticate(email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError('Невозможно войти с предоставленными учетными данными.')

        data['user'] = user
        return data
