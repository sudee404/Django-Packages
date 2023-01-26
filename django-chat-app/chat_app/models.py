from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    file = models.FileField(upload_to='chat_files', blank=True, null=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    @property
    def is_owner(self):
        return self.sender == self.request.user

class ChatRoom(models.Model):
    """Model for chat room

    """
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(get_user_model())
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    def get_absolute_url(self):
        return reverse("chat-view", kwargs={"room_name": self.id})
