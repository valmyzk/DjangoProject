import decimal
from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Wallet
from django.contrib import messages


# Create your views here.
def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')

@login_required
def buy(request: HttpRequest) -> HttpResponse:
    return render(request, 'buy.html')

@login_required
def sell(request: HttpRequest) -> HttpResponse:
    return render(request, 'sell.html')

@login_required
def add_funds(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)
        except (ValueError, TypeError, decimal.InvalidOperation):
            amount = None

        if amount and amount > 0:
            wallet = Wallet.objects.get(user=request.user)
            wallet.amount += amount
            wallet.save()

            messages.success(request, f"Funds added successfully! New balance: €{wallet.amount}")
        else:
            messages.error(request, "Please enter a valid amount.")

        return redirect('add_funds')  # Redirect back to the page with success or error message

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
