from django.urls import path
from django.http import HttpResponse
from .views import CreateUserView, UsersViewSet, CustomAuth
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# schema_view = get_schema_view(
#     openapi.Info(
#         title="User API",
#         default_version='v1',
#         description="API для работы с пользователями",
#     ),
#     public=True,
#     permission_classes=(AllowAny,),
# )


# # Создаем функцию-заглушку, которая возвращает пустой ответ
# def placeholder_view(request):
#     return HttpResponse("Placeholder")

urlpatterns = [
    # path('', placeholder_view, name='placeholder'),  # Заглушка по основному пути
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('get-user/', UsersViewSet.as_view(), name='get_user'),
    path('login/', CustomAuth.as_view(), name='login'),
]