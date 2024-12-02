from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Room, Participant
from .serializers import RoomSerializer
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class RoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["room"],
        summary="Создание комнаты",
        responses={201: RoomSerializer}
    )
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            Participant.objects.create(userId=request.user, roomId=room, score=0)
            return Response({
                'success': 'Комната создана',
                'room_id': room.id,
                'quiz_subject': room.quizSubject,
                'timer': room.timer,
                'invitation_code': room.invitation_code,
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # @extend_schema(
    #     tags=["room"],
    #     summary="Получить все комнаты",
    #     responses={200: RoomSerializer(many=True)}
    # )
    # def get(self, request):
    #     rooms = Room.objects.all()
    #     serializer = RoomSerializer(rooms, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @extend_schema(
    #     tags=["room"],
    #     summary="Обновить данные комнаты",
    #     responses={200: RoomSerializer}
    # )
    # def put(self, request, room_id):
    #     try:
    #         room = Room.objects.get(id=room_id)
    #     except Room.DoesNotExist:
    #         return Response({'error': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = RoomSerializer(room, data=request.data, partial=True)  # partial=True для частичного обновления
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'success': 'Данные комнаты обновлены',
    #             'room': serializer.data
    #         }, status=status.HTTP_200_OK)
    #     return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # @extend_schema(
    #     tags=["room"],
    #     summary="Удалить комнату",
    #     responses={204: None}
    # )
    # def delete(self, request, room_id):
    #     try:
    #         room = Room.objects.get(id=room_id)
    #     except Room.DoesNotExist:
    #         return Response({'error': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

    #     room.delete()
    #     return Response({'success': 'Комната удалена'}, status=status.HTTP_204_NO_CONTENT)
    

# @login_required
# def create_room(request):
#     if request.method == 'POST':
#         # quiz_subject = request.POST.get('quizSubject')
#         # timer = int(request.POST.get('timer', 30))

#         # room = Room.objects.create(quizSubject=quiz_subject, timer=timer)
#         # Participant.objects.create(userId=request.user, roomId=room, score=0)
        
        
#         # return JsonResponse({
#         #     'success': 'Комната создана',
#         #     'room_id': room.id,
#         #     'quiz_subject': room.quizSubject,
#         #     'timer': room.timer
#         # })
#         serializer = RoomSerializer(data=request.data)
#         if serializer.is_valid():
#             room = serializer.save()
#             Participant.objects.create(userId=request.user, roomId=room, score=0)
#             return Response({
#                 'success': 'Комната создана',
#                 'room_id': room.id,
#                 'quizSubject': room.quizSubject,
#                 'timer': room.timer
#             }, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
