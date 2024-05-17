from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    USER = 'User'
    BOT = 'Bot'
    SENDER_CHOICES = [
        (USER, 'User'),
        (BOT, 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.sender}) - {self.created_at}: {self.text}"
