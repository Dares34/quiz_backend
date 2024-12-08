import json
import logging

logger = logging.getLogger(__name__)
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
class RoomConsumer(AsyncConsumer):
    async def websocket_connect(self):
        logger.info(f"Attempting to connect to room: {self.scope['url_route']['kwargs']}")
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        # Добавляем WebSocket в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем WebSocket из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получаем сообщение из WebSocket
    async def websocket_receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['action'] == 'join':
            participant_name = text_data_json['name']
            # Логика добавления участника
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "player_update",
                    "action": "join",
                    "name": participant_name,
                }
            )

    # Обрабатываем сообщение из группы
    async def chat_message(self, event):
        message = event['message']

        # Отправляем сообщение в WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
    
    async def player_update(self, event):
        action = event["action"]
        name = event["name"]

        await self.send(text_data=json.dumps({
            "action": action,
            "name": name,
        }))