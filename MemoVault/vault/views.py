from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentForm


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = {'form': DocumentForm()}
    return render(request, "vault/index.html", form)
