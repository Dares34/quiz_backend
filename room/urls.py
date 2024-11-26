from django.urls import path
from django.http import HttpResponse
from . import views
from .models import Room
from .views import CreateRoomView

def placeholder_view(request):
    return HttpResponse("Placeholder")

urlpatterns = [
    path('', placeholder_view, name='placeholder'),
    # path('rooms/create-room', views. name='room_settings'),
    path('create-room/', CreateRoomView.as_view(), name='create_room'),
]
