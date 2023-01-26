import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_app.models import ChatRoom, Message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.save_message_db(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message,"sender": self.scope["user"].email}
        )

    # Save message to the database
    @database_sync_to_async
    def save_message_db(self, message):
        """Saves the message to the database

        Args:
            message (str): Message sent
        """
        user = get_user_model().objects.get(pk=self.scope["user"].id)
        chat_room = ChatRoom.objects.get(name=self.room_name)
        message_obj = Message.objects.create(
            sender=user, content=message, chat_room=chat_room)
        message_obj.save()

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
