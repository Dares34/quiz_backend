from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, AuthView

router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),  # Новый путь для авторизации
]
