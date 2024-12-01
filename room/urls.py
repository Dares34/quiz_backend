from django.urls import path
from django.http import HttpResponse
from . import views
from rest_framework.routers import DefaultRouter
from .models import Room
from .views import RoomAPIView

router = DefaultRouter()
router.register(r'rooms', RoomAPIView, basename='room')

# def placeholder_view(request):
#     return HttpResponse("Placeholder")

urlpatterns = [
    # path('', placeholder_view, name='placeholder'),
    # path('rooms/create-room', views. name='room_settings'),
    path('room/', RoomAPIView.as_view(), name='rooms'),
    path('rooms/<int:room_id>/', RoomAPIView.as_view()),
]
