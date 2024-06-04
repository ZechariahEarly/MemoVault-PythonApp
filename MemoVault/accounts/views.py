from django.shortcuts import render, redirect

from .forms import CreateUserForm


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO:log the user in
            return redirect('vault:index')
        else:
            print(form.errors)
    else:
        form = {'form': CreateUserForm()}
    return render(request, 'accounts/signup.html', {'form': form})