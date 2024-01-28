from .models import ChatMessage
from rest_framework.response import Response
from .serializers import ChatMessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_chat_messages(request):
    chat_messages = ChatMessage.objects.all()
    serializer = ChatMessageSerializer(chat_messages, many=True)
    return Response(
        {
            "success": True,
            "chat_messages": serializer.data
        },
        status=status.HTTP_200_OK)


"""

For Chats:
Use the names of the sender and the receiver to create a chat room
If chat room loads, fetch the previous chats from the server.
Use the names of the sender and the receiver to create a chat room (ws connection)
When sender sends a message, save the msg to the database and broadcast to the chat room.
"""
