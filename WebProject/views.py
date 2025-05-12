import decimal
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import EditProfileForm
from .models import Wallet


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

import logging
log = logging.getLogger(__name__)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, initial=model_to_dict(user))
        if form.is_valid():
            user.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.phone = form.cleaned_data.get('phone')
            user.save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(initial=model_to_dict(user))
    return render(request, 'edit_profile.html', {'form': form})
