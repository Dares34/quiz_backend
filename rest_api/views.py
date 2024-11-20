from django.http import HttpRequest
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate


class UsersViewSet(APIView):
    @extend_schema(
        request=UserSerializer,
        parameters=[
            OpenApiParameter(
                name='email',
                required=True
            ), OpenApiParameter(
                name='password',
                required=True
            )
        ],
        responses={201: UserSerializer, 403: "Неправильный логин или пароль"}
    )
    def get(self, request: HttpRequest):
        email = request.GET.get('email', None)
        password = request.GET.get('password', None)
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response('Wrong email or password', status=403)
        return Response({
            'name': user.name,
            'email': user.email,
            'role': user.role.name,  # или другой атрибут роли
        })


class CreateUserView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: "Ошибка валидации"}
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
