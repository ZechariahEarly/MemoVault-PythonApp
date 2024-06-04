from pyexpat.errors import messages

from django import forms

from .models import Document
from django.contrib.auth.forms import get_user_model


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'file')


