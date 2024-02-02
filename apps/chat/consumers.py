import json
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from .models import Chat, ChatMessage


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract the token from the query string
        query_string = scope.get('query_string', b'').decode('utf-8')
        token_param = next((param.split('=') for param in query_string.split('&') if param.startswith('token=')), None)

        if token_param:
            try:
                # Attempt to authenticate the user using the token
                scope['user'] = await database_sync_to_async(self.authenticate_user)(token_param[1])

            except Exception as e:
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def authenticate_user(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            raise Exception("Invalid token")


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        self.group_name = None
        self.chat_id = None

    async def connect(self):

        self.chat_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f'room_{self.chat_id}'
        if self.scope['user'].is_authenticated:
            # Join room group
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            # mark read Messages
            await database_sync_to_async(self.mark_read)(self.scope['user'])

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # implement save msg
        chat_message = await database_sync_to_async(self.save_message)(message, self.scope['user'])

        event = {
            "type": "chat_message",
            "sender": self.scope['user'].id,
            "message": message,
            "date": timezone.localtime(chat_message.date).strftime('%Y-%m-%d %H:%M:%S')
        }


        # Send message to room group
        await self.channel_layer.group_send(self.group_name, event)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "chat",
            "sender": event["sender"],
            "message": message,
            "date": event['date']
        }))


    def save_message(self, message_text, sender):
        # Get the chat object based on the chat_id
        chat = Chat.objects.get(id=self.chat_id)

        # Save the message to the database
        chat_message = ChatMessage.objects.create(
            chat=chat,
            sender=sender,
            message=message_text
        )
        return chat_message

    def mark_read(self, user):
        chat = Chat.objects.get(id=self.chat_id)
        unread_messages = chat.messages.exclude(sender=user).exclude(is_read=True)
        if unread_messages:
            for msg in unread_messages:
                msg.is_read = True
                msg.save()



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
