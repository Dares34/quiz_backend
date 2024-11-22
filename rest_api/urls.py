from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, AuthView, CreateUserView
from room.views import RoomViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='user')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', AuthView.as_view(), name='auth'),  # Новый путь для авторизации
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('rooms/<int:pk>/add_participant/', RoomViewSet.as_view({'post': 'add_participant'}), name = 'add_participant'),
    path('rooms/<int:pk>/remove_participant/', RoomViewSet.as_view({'post': 'remove_participant'}), name = 'remove_participant'),
    # path('rooms/', RoomViewSet.as_view(), name='create_room'),
]
