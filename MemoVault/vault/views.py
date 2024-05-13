from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentForm

def index(request):
    context = {'form': DocumentForm()}
    return render(request, "vault/index.html", context)
# Create your views here.
