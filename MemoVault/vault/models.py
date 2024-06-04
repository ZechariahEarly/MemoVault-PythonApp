import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# def user_directory_path(user, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(user.id, filename)

class Document (models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField( max_length=500) #upload_to=user_directory_path(User, name)
    location = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name, self.location



