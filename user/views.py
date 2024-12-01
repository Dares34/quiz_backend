from django.shortcuts import render
from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate

class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="Описание ошибки")

class UsersViewSet(APIView):

    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags = ["user"],
        summary = "Получение текущего ползователя",
        
        responses={200: UserSerializer}
        # request=UserSerializer,
        # parameters=[
        #     OpenApiParameter(
        #         name='email',
        #         required=True
        #     ), OpenApiParameter(
        #         name='password',
        #         required=True
        #     )
        # ],
        # responses={201: UserSerializer, 403: "Неправильный логин или пароль"}
    )
    def get(self, request: HttpRequest):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        # email = request.GET.get('email', None)
        # password = request.GET.get('password', None)
        # user = authenticate(request, email=email, password=password)
        # if not user:
        #     return Response('Wrong email or password', status=403)
        # return Response({
        #     'name': user.name,
        #     'email': user.email,
        #     'role': user.role.name,  # или другой атрибут роли
        # })


class CreateUserView(APIView):
    @extend_schema(
        tags = ["user"],
        summary="Создание пользователя",
        request=UserSerializer,
        responses={201: UserSerializer, 400: ErrorResponseSerializer}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'email': user.email,
                'name': user.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    