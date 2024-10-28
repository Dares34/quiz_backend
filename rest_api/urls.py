from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, AuthView, CreateUserView

router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),  # Новый путь для авторизации
    path('create_user/', CreateUserView.as_view(), name='create_user'),
]
