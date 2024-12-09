from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Room, redis_client
from .serializers import RoomSerializer, RoomStatusSerializer, AddParticipantSerializer, IncrementScoreSerializer
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from django_redis import get_redis_connection
import  json

class CreateRoomView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    @extend_schema(
        tags=["room"],
        summary="Создать команту",
        responses={200: RoomSerializer(many=True)}
    )
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            room.assign_questions_by_subject()
            return Response(
                {
                    "success": "Комната успешно создана",
                    "room": serializer.data
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    @receiver(post_save, sender = Room)
    def create_room_session(sender, instance, created, **kwargs):
        if created:
            instance.create_session_in_redis()


class AddParticipantView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AddParticipantSerializer

    @extend_schema(
        tags=["room"],
        summary="Добавить участника в комнату",
        description="Добавляет участника в указанную комнату по ID комнаты.",
        request=AddParticipantSerializer,
        responses={
            200: {"type": "object", "properties": {"success": {"type": "string"}}},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}},
        }
    )
    def post(self, request, room_id):
        serializer = AddParticipantSerializer(data=request.data)
        if serializer.is_valid():
            participant_id = serializer.validated_data["participant_id"]
            participant_name = serializer.validated_data["participant_name"]

            try:
                room = Room.objects.get(id=room_id)
            except Room.DoesNotExist:
                return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
            try:
                user = User.objects.get(id=participant_id)
            except User.DoesNotExist:
                return Response({"error": "Пользователь не существует"}, status=status.HTTP_404_NOT_FOUND)

            session_key = f"room:{room.id}"
            participants = json.loads(redis_client.hget(session_key, "participants") or "[]")
            if len(participants) >= 4:
                return Response({"error": "В комнате уже 4 участника"}, status=status.HTTP_400_BAD_REQUEST)

            if any(p["id"] == participant_id for p in participants):
                return Response({"error": f"Участник {participant_name} уже в комнате"}, status=status.HTTP_400_BAD_REQUEST)

            participants.append({"id": participant_id, "name": participant_name})
            redis_client.hset(session_key, "participants", json.dumps(participants))

            return Response({"success": f"Участник {participant_name} добавлен в комнату {room_id}"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncrementScoreView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    serializer_class = IncrementScoreSerializer
    @extend_schema(
        tags=["room"],
        summary="Увеличить очки участника",
        description="Увеличивает очки указанного участника в комнате на заданное количество.",
        request=IncrementScoreSerializer,
        responses={
            200: {"type": "object", "properties": {"success": {"type": "string"}}},
            404: {"type": "object", "properties": {"error": {"type": "string"}}},
        }
    )
    def post(self, request, room_id):
        serializer = IncrementScoreSerializer(data=request.data)
        if serializer.is_valid():
            participant_id = serializer.validated_data["participant_id"]
            score = serializer.validated_data["score"]
            try:
                room = Room.objects.get(id=room_id)
                room.increment_score(participant_id, score)
                return Response({"success": f"Очки увеличены для участника {participant_id} в комнате {room_id}"}, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoomStatusView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RoomStatusSerializer
    @extend_schema(
        tags=["room"],
        summary="Просмотреть параметры комнаты",
        parameters=[
            OpenApiParameter(
                name="room_id",
                description="id комнаты",
                required=True,
                type=int,
                location=OpenApiParameter.QUERY
            ),
        ],
        responses={200: RoomStatusSerializer}
    )
    def get(self, request):
        room_id = request.query_params.get('room_id')
        room_data = Room.get_room_data(room_id)
        if not room_data:
            return Response({'error':"Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"room_data":room_data})


class DeleteRoomView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    serializer_class = RoomSerializer

    @extend_schema(
        tags=["room"],
        summary="Удалить комнату",
        responses={200: RoomSerializer}
    )
    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            room.delete()
            return Response(
                {"success": f"Комната с ID {pk} успешно удалена"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Room.DoesNotExist:
            return Response(
                {"error": f"Комната с ID {pk} не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )    

    @receiver(post_delete, sender=Room)
    def delete_room_session(sender, instance, **kwargs):
        instance.delete_session_in_redis()

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
