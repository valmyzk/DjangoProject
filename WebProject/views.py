from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')

def buy(request: HttpRequest) -> HttpResponse:
    return render(request, 'buy.html')

def sell(request: HttpRequest) -> HttpResponse:
    return render(request, 'sell.html')

def add_funds(request: HttpRequest) -> HttpResponse:
    return render(request, 'add_funds.html')

def transfer_funds(request: HttpRequest) -> HttpResponse:
    return render(request, 'transfer_funds.html')

def my_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'my_profile.html')