from django.urls import path
from .views import CreateRoomView, DeleteRoomView, RoomStatusView
from .views import AddParticipantView, IncrementScoreView

urlpatterns = [
    path('create/', CreateRoomView.as_view(), name='create-room'),
    path('delete/<int:pk>/', DeleteRoomView.as_view(), name='delete-room'),
    path('roomView/', RoomStatusView.as_view(), name='room-view'),
    path('<int:room_id>/add-participant/', AddParticipantView.as_view(), name='add-participant'),
    path('<int:room_id>/increment-score/', IncrementScoreView.as_view(), name='increment-score'),
]