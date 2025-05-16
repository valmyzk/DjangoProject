from django.contrib import auth
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserCreationForm


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth.login(request, form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('root')
