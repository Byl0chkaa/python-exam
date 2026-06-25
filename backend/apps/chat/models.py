from django.conf import settings
from django.db import models

from apps.ads.models import CarAdModel


class ChatRoomModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_private = models.BooleanField(default=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    ad = models.ForeignKey(CarAdModel, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)

class MessageModel(models.Model):
    room = models.ForeignKey(ChatRoomModel, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']