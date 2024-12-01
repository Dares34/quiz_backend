from django.urls import path
from django.http import HttpResponse
from .views import CreateUserView, UsersViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="User API",
        default_version='v1',
        description="API для работы с пользователями",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


# Создаем функцию-заглушку, которая возвращает пустой ответ
def placeholder_view(request):
    return HttpResponse("Placeholder")
urlpatterns = [
    path('', placeholder_view, name='placeholder'),  # Заглушка по основному пути
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('get_user/', UsersViewSet.as_view(), name='current-user'),
]