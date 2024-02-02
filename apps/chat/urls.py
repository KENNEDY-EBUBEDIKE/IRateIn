from django.urls import path
from django.conf import settings
from .views import get_chats, create_chat, get_chat_messages


urlpatterns = [
    path('get-chats/', get_chats, name='get_chats'),
    path('create-chat/', create_chat, name='create_chat'),
    path('get-chat-messages/', get_chat_messages, name='get_chat_messages'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
