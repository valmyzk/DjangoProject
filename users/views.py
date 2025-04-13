from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth

# Create your views here.
def signup(request):
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