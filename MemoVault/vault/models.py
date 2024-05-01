from django.db import models

# Create your models here.

class User (models.Model):
    name = models.CharField(max_length=80)
    openai_api_key = models.CharField(max_length=57)
    def __str__(self):
        return self.name, self.openai_api_key

class Document (models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name, self.location
