from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_user

# Create your views here.


def register(request):
    # if request.user.is_authenticated:
    #     raise Exception('Seems like you are already logged in.')
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    logout_user(request)
    return redirect('/')

