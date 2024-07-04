from django.urls import path, include

from . import views
from .views import ChatView

app_name = 'chat'

urlpatterns = [
    path("", ChatView.index, name="chat"),
    path('clear_chat', ChatView.clear_chat, name='clear_chat'),
    path('add_conversation', ChatView.add_conversation, name='add_conversation'),
]