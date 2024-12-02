from django.urls import path
from .views import CreateRoomView, DeleteRoomView

urlpatterns = [
    path('create/', CreateRoomView.as_view(), name='create-room'),
    path('delete/<int:pk>/', DeleteRoomView.as_view(), name='delete-room'),
]