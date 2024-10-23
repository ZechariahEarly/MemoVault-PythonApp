from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import CreateUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CreateUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO:log the user in
            return redirect('vault:vault')
        else:
            print(form.errors)
    else:
        form = {'form': CreateUserCreationForm()}
    return render(request, 'accounts/signup.html', {'form': form})

