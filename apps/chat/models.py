from django.db import models


class ChatMessage(models.Model):
    message = models.TextField(blank=False, null=False)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='received_messages')
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.message}'

    def __unicode__(self):
        return f'{self.sender} to {self.receiver} - {self.message}'

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
