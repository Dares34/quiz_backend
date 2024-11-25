from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, CreateUserView
from .views import CreateRoomView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('get_user/', UsersViewSet.as_view(), name='get_user'),
    path('create_room/', CreateRoomView.as_view(), name='create_room')
]
