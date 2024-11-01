from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, AuthView, CreateUserView, RoomViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),  # Новый путь для авторизации
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    # path('rooms/', RoomViewSet.as_view(), name='create_room'),
]
