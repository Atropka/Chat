from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)  # Добавляем связь с Chat
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)  # Поле для файла

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']