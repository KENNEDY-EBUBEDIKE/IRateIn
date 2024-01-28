import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        self.group_name = None

    async def connect(self):

        self.group_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        event = {
            "type": "chat_message",
            "message": message
        }

        # Send message to room group
        await self.channel_layer.group_send(self.group_name, event)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": message
        }))




# class NotificationConsumer(AsyncWebsocketConsumer):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#
#         self.group_name = "notification"
#
#     async def connect(self):
#
#         # Join room group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()
#         # await self.per_send()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#
#     async def per_send(self):
#         for i in range(1, 11):
#             await asyncio.sleep(2)
#             await self.send(text_data=json.dumps({
#                 "type": "notification",
#                 "message": f'This is number {i} Message',
#             }))
#         await self.close()
