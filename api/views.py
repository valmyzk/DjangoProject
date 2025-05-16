
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from WebProject.models import Asset
import json


# Create your views here.
@login_required
def all_assets(request: HttpRequest) -> HttpResponse:
    response = HttpResponse()
    json.dump([{'name': asset.name, 'symbol': asset.symbol, 'type': asset.type} for asset in Asset.objects.all()], response)
    return response

@login_required
def asset(request: HttpRequest, symbol: str) -> HttpResponse:
    response = HttpResponse()
    json.dump(model_to_dict(get_object_or_404(Asset, symbol=symbol)), response)
    return response

@login_required
def asset_price(request: HttpRequest, symbol: str) -> HttpResponse:
    # Parse period
    try:
        period = int(request.GET.get('period', 1))
    except ValueError:
        return HttpResponseBadRequest('period must be an integer')

    # Get historical data
    response = HttpResponse()
    json.dump(get_object_or_404(Asset, symbol=symbol).price_history(period), response)
    return response