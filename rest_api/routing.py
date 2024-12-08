from django.urls import path, include

websocket_urlpatterns = [
    path("rooms/", include('room.routing')),
]