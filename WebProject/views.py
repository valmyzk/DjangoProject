from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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
@login_required

def transfer_funds(request: HttpRequest) -> HttpResponse:
    return render(request, 'transfer_funds.html')
@login_required
def my_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'my_profile.html')

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('my_profile')  # Asumiendo que tienes esa URL

    return render(request, 'edit_profile.html', {'user': user})
