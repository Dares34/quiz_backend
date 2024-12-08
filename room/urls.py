from django.urls import path
from .views import CreateRoomView, DeleteRoomView, RoomStatusView

urlpatterns = [
    path('create/', CreateRoomView.as_view(), name='create-room'),
    path('delete/<int:pk>/', DeleteRoomView.as_view(), name='delete-room'),
    path('roomView/', RoomStatusView.as_view(), name='room-view')
]