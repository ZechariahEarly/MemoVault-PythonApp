from django import forms
from django.contrib.auth import get_user_model

from .models import User


class CreateUserForm(forms.ModelForm):
    User = get_user_model()
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'openai_api_key')