from django.core.exceptions import ObjectDoesNotExist
from .models import ChatMessage, Chat
from apps.users.models import User
from apps.users.serializers import UserSerializer
from .serializers import ChatMessageSerializer, ChatSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_chats(request):
    user_chats = Chat.objects.filter(participants=request.user)
    chats_data = []

    for chat in user_chats:
        if chat.messages.first():
            other_participant = chat.participants.exclude(id=request.user.id).first()
            last_message = chat.messages.first()
            unread_mgs = chat.messages.exclude(sender=request.user).exclude(is_read=True).count()
            chat_info = {
                'chat_id': chat.id,
                'user_id': request.user.id,
                'participant': UserSerializer(other_participant).data,
                'last_message': ChatMessageSerializer(last_message).data,
                'unread_mgs': unread_mgs,
            }
            chats_data.append(chat_info)
        else:
            continue
    return Response(
        {
            "success": True,
            "chats": chats_data
        },
        status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_chat_messages(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])

    chat_messages = chat.messages.all().order_by('date')

    return Response(
        {
            "success": True,
            "chatMessages": ChatMessageSerializer(chat_messages, many=True).data
        },
        status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_chat(request):
    user_a = request.user
    if user_a.email == request.data['email']:
        return Response(
            {
                "success": False,
                "error": "You can add Yourself"
            },
            status=status.HTTP_200_OK
        )

    try:
        user_b = User.objects.get(email=request.data['email'])
    except ObjectDoesNotExist:
        return Response(
            {
                "success": False,
                "error": "Not a Registered User"
            },
            status=status.HTTP_200_OK
        )

    # Check if a chat between these users already exists
    chat = Chat.objects.filter(participants=user_a).filter(participants=user_b).first()

    if not chat:
        # If the chat doesn't exist, create a new one
        chat = Chat.objects.create()
        chat.participants.add(user_a, user_b)
    return Response(
            {
                "success": True,
                "chat": ChatSerializer(chat).data,
            },
            status=status.HTTP_200_OK)

"""
For Chats:
Use the chat_id to create a chat room
If chat room loads, fetch the previous chats from the server.
When sender sends a message, save the msg to the database and broadcast to the chat room.
when ws conn is established, get msgs recd by req.user that are unread and mark as read.
Use the inbox opening to establish notification connection.

"""
