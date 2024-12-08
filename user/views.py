from django.shortcuts import render
from django.http import HttpRequest
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer, AuthSerializer
from django.contrib.auth import authenticate


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="Описание ошибки")


class UsersViewSet(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["user"],
        summary="Получение текущего ползователя",
        parameters=[
            OpenApiParameter(
                name="email",
                description="Электронная почта пользователя",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name="password",
                description="Пароль пользователя",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={200: UserSerializer}
    )
    def get(self, request: HttpRequest):
        email = request.GET.get('email')
        password = request.GET.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            return Response({"detail": "Пользователь не зарегистрирован или данные неверны"}, status=401)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class CreateUserView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    @extend_schema(
        tags=["user"],
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
                'name': user.name,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuth(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        tags=['user'],
        summary="Авторизация пользователя",
        request=AuthSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'user_id': user.id,
            'email': user.email,
        })


class IncrementWinsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(description="Запрос на увеличение количества побед пользователя по email")
    def post(self, request: HttpRequest):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email не предоставлен"}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)
        user.wins += 1
        user.save()
        return Response({"email": user.email, "wins": user.wins}, status=200)