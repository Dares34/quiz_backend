from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Room, Participant
from user.models import User

@login_required
def create_room(request):
    if request.method == 'POST':
        quiz_subject = request.POST.get('quizSubject')
        timer = int(request.POST.get('timer', 30))

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
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, roomId=room, userId=request.user)

    if participant.userId != request.user:
        return JsonResponse({'error': 'Только владелец комнаты может изменять настройки'}, status=403)

    # Обновить тему викторины и таймер, если она в запросе
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
    room = get_object_or_404(Room, id=room_id)
    participant = get_object_or_404(Participant, roomId=room, userId=request.user)

    if participant.userId != request.user:
        return JsonResponse({'error': 'Только владелец комнаты может запустить игру'}, status=403)
    
    return JsonResponse({'success': 'Игра начата'})

@login_required
def get_room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    participants = Participant.objects.filter(roomId=room).select_related('userId')
    participant_list = [{'name': p.userId.name, 'score': p.score} for p in participants]

    return JsonResponse({
        'room_id': room.id,
        'quiz_subject': room.quizSubject,
        'timer': room.timer,
        'participants': participant_list
    })
