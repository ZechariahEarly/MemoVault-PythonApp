from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Document

from .forms import DocumentForm


class VaultView(View):
    @login_required
    def index(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
            else:
                print(form.errors)
            context = {'form': DocumentForm(), 'files': VaultView.get_vault_files(request)}
        if request.method == 'GET':
            context = {'form': DocumentForm(), 'files': VaultView.get_vault_files(request)}
        return render(request, "vault/vault.html", context)


    def get_vault_files(request):
        return (Document.objects.filter(user=request.user)
                .filter(file__isnull=False)
                )
