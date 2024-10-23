from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CreateUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'openai_api_key')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'openai_api_key')