from django.db import models


class Chat(models.Model):
    participants = models.ManyToManyField('users.User')
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_chats')
    message = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} - {self.message}'

    def __unicode__(self):
        return f'{self.sender} - {self.message}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'

        indexes = [
            models.Index(fields=['date', ]),
        ]

        managed = True
        db_table = 'chat_message'
        app_label = 'chat'
