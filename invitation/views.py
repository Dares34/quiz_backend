from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from room.models import Room, Participant
from user.models import User
from .models import Invitation

@login_required
def invite_user(request, room_id):
    # Retrieve the room or return 404 if it doesn't exist
    room = get_object_or_404(Room, id=room_id)

    # Check if the room is already full
    current_participants_count = Participant.objects.filter(roomId=room).count()
    if current_participants_count >= 4:
        return JsonResponse({'error': 'Комната уже заполнена'}, status=400)

    # Retrieve the user to invite from the request data
    invited_user_id = request.POST.get('invited_user_id')
    invited_user = get_object_or_404(User, id=invited_user_id)

    # Ensure the invited user is not already in the room
    if Participant.objects.filter(roomId=room, userId=invited_user).exists():
        return JsonResponse({'error': 'Пользователь уже в комнате'}, status=400)

    # Create or get the invitation instance
    invitation, created = Invitation.objects.get_or_create(room=room, invited_user=invited_user)
    if created:
        message = f'Приглашение отправлено пользователю {invited_user.name}'
    else:
        message = f'Приглашение уже существует для пользователя {invited_user.name}'

    return JsonResponse({'success': message})
