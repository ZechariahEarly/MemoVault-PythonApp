from django.shortcuts import render

from django.http import HttpResponse


def hero(request):
    return render(request, 'hero.html')
