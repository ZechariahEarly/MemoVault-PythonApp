from django.conf import settings
from django.db import models

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)