from django.urls import path
from .consumers import RoomConsumer

websocket_urlpatterns = [
    # path("<str:room_code>/", RoomConsumer.as_asgi()),
    path("ws/rooms/<str:room_code>/", RoomConsumer.as_asgi()),
]