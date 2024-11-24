from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Room, Participant
from user.models import User

@login_required
def create_room(request):
    if request.method == 'POST':
        # Room creation and user assignment as the room owner
        quiz_subject = request.POST.get('quizSubject')
        timer = int(request.POST.get('timer', 30))  # default to 30 seconds if not set

        room = Room.objects.create(quizSubject=quiz_subject, timer=timer)
        Participant.objects.create(userId=request.user, roomId=room, score=0)

        return JsonResponse({
            'success': 'Комната создана',
            'room_id': room.id,
            'quiz_subject': room.quizSubject,
            'timer': room.timer
        })

@login_required
@require_POST
def update_room_settings(request, room_id):
    # Only the room owner can update settings
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, roomId=room, userId=request.user)

    if participant.userId != request.user:
        return JsonResponse({'error': 'Только владелец комнаты может изменять настройки'}, status=403)

    # Update quiz subject and timer if provided in request
    quiz_subject = request.POST.get('quizSubject')
    timer = request.POST.get('timer')

    if quiz_subject:
        room.quizSubject = quiz_subject
    if timer:
        room.timer = int(timer)
    room.save()

    return JsonResponse({'success': 'Настройки комнаты обновлены'})

@login_required
@require_POST
def start_game(request, room_id):
    # Only the room owner can start the game
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, roomId=room, userId=request.user)

    if participant.userId != request.user:
        return JsonResponse({'error': 'Только владелец комнаты может запустить игру'}, status=403)

    # Game start logic here
    # Send notifications or update status to indicate game start if needed
    return JsonResponse({'success': 'Игра начата'})

@login_required
def get_room_details(request, room_id):
    # Retrieve room details for display
    room = get_object_or_404(Room, id=room_id)
    participants = Participant.objects.filter(roomId=room).select_related('userId')
    participant_list = [{'name': p.userId.name, 'score': p.score} for p in participants]

    return JsonResponse({
        'room_id': room.id,
        'quiz_subject': room.quizSubject,
        'timer': room.timer,
        'participants': participant_list
    })
