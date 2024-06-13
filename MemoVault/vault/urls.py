from django.urls import path, include

from . import views
from .views import VaultView

app_name = 'vault'

urlpatterns = [
    path("", VaultView.index, name="vault")
]