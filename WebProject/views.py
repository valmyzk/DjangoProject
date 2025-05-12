import logging

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import EditProfileForm, AddFundsForm, TransferFundsForm
from .models import Transaction
from .utils import transfer_funds_internal, get_admin

logger = logging.getLogger(__name__)


# Create your views here.
def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'dashboard/wallet.html')
    return render(request, 'landing.html')


@login_required
def cash(request: HttpRequest) -> HttpResponse:
    wallet = request.user.wallet
    transactions = Transaction.objects.filter(Q(source=wallet) | Q(destination=wallet)).order_by('-datetime')[:5]
    return render(request, 'dashboard/cash.html', {'transactions': transactions})


@login_required
def buy(request: HttpRequest) -> HttpResponse:
    return render(request, 'operations/buy.html')


@login_required
def sell(request: HttpRequest) -> HttpResponse:
    return render(request, 'operations/sell.html')


@login_required
def add_funds(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            transfer_funds_internal(get_admin().wallet, request.user.wallet, form.cleaned_data['amount'])
            return redirect('/')
    else:
        form = AddFundsForm()
    return render(request, 'transactions/add_funds.html', {'form': form})


@login_required
def transfer_funds(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TransferFundsForm(request.user, request.POST)
        if form.is_valid():
            # Form validation guarantees enough balance (ignoring TOCTOU...)
            transfer_funds_internal(request.user.wallet, form.wallet, form.cleaned_data['amount'])
            return redirect('/')
    else:
        form = TransferFundsForm(request.user)
    return render(request, 'transactions/transfer_funds.html', {'form': form})


@login_required
def my_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'profile/my_profile.html')


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
    return render(request, 'profile/edit_profile.html', {'form': form})
