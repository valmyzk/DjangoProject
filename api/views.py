import json

from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from functools import lru_cache

from django.db.models import Sum, Q
from collections import defaultdict

from WebProject.models import Asset, Holding, Transaction


# Create your views here.
@login_required
def all_assets(request: HttpRequest) -> HttpResponse:
    response = HttpResponse()
    json.dump([{'name': asset.name, 'symbol': asset.symbol, 'type': asset.type} for asset in Asset.objects.all()],
              response)
    return response

def get_holdings_for_user(user):
    """
    Get current holdings for a user with calculated values
    """
    holdings = Holding.objects.filter(user=user).select_related('asset')
    holdings_data = []

    for holding in holdings:
        # Calculate current value (assuming Asset has a price field)
        current_value = float(holding.amount) * float(holding.asset.price)

        holdings_data.append({
            'symbol': holding.asset.symbol,
            'amount': float(holding.amount),
            'value': current_value,
            'asset': {
                'symbol': holding.asset.symbol,
                'name': holding.asset.name,
                'price': float(holding.asset.price),
                'stock_change': 0  # You can calculate this based on historical data
            }
        })

    return holdings_data


def get_portfolio_history_simple(user, start_date, end_date):
    """
    Simple portfolio history based on current holdings
    Since your Transaction model is for wallet transfers, not stock trades
    """

    # Get current holdings
    current_holdings = get_holdings_for_user(user)
    current_total = sum(holding['value'] for holding in current_holdings)

    if current_total == 0:
        # Return empty portfolio if no holdings
        return {
            'labels': [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')],
            'values': [0, 0]
        }

    # Generate dates (weekly points for smoother chart)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=7)

    # If we only have one date, add the end date
    if len(dates) == 1:
        dates.append(end_date)

    # Create realistic portfolio growth simulation
    # You can make this more sophisticated later
    values = []
    for i, date in enumerate(dates):
        if len(dates) == 1:
            values.append(current_total)
        else:
            progress = i / (len(dates) - 1)
            # Simulate portfolio starting at 70% of current value with some volatility
            base_value = current_total * (0.7 + 0.3 * progress)

            # Add some realistic volatility (±5%)
            import random
            volatility = random.uniform(-0.05, 0.05) if i > 0 else 0
            value = base_value * (1 + volatility)
            values.append(round(max(value, 0), 2))

    return {
        'labels': [date.strftime('%Y-%m-%d') for date in dates],
        'values': values
    }


@login_required
def portfolio_history_api(request):
    """
    API endpoint for portfolio history
    """
    period = request.GET.get('period', '6M')
    user = request.user

    # Calculate date range based on period
    end_date = timezone.now().date()
    if period == '1D':
        start_date = end_date - timedelta(days=1)
    elif period == '1W':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1M':
        start_date = end_date - timedelta(days=30)
    elif period == '3M':
        start_date = end_date - timedelta(days=90)
    elif period == '6M':
        start_date = end_date - timedelta(days=180)
    elif period == '1Y':
        start_date = end_date - timedelta(days=365)
    else:  # ALL
        start_date = user.date_joined.date()

    try:
        portfolio_data = get_portfolio_history_simple(user, start_date, end_date)
    except Exception as e:
        # Fallback data in case of errors
        portfolio_data = {
            'labels': [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')],
            'values': [0, 0]
        }

    return JsonResponse({
        'labels': portfolio_data['labels'],
        'values': portfolio_data['values']
    })


@login_required
def holdings_api(request):
    """
    API endpoint for current holdings
    """
    user = request.user
    holdings_data = get_holdings_for_user(user)
    return JsonResponse(holdings_data, safe=False)

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


@login_required
def holdings(request: HttpRequest) -> HttpResponse:
    holdings = Holding.objects.filter(user=request.user)
    response = HttpResponse()
    json.dump([{'symbol': holding.asset.symbol, 'amount': float(holding.amount)} for holding in holdings], response)
    return response


# Additional utility functions you might need

@login_required
def portfolio_metrics_api(request):
    """
    Get current portfolio metrics (total value, daily change, etc.)
    """
    user = request.user
    holdings_data = get_holdings_for_user(user)

    current_value = sum(holding['value'] for holding in holdings_data)

    # Simple daily change calculation (you can enhance this)
    # For now, simulate a small random change
    import random
    daily_change = current_value * random.uniform(-0.02, 0.02)  # ±2% change
    daily_change_percent = (daily_change / current_value * 100) if current_value > 0 else 0

    return JsonResponse({
        'current_value': round(current_value, 2),
        'daily_change': round(daily_change, 2),
        'daily_change_percent': round(daily_change_percent, 2),
        'total_holdings': len(holdings_data)
    })


def get_user_wallet_balance(user):
    """
    Calculate user's total wallet balance from transactions
    """
    # Money received (destination transactions)
    received = Transaction.objects.filter(
        destination__user=user
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Money sent (source transactions)
    sent = Transaction.objects.filter(
        source__user=user
    ).aggregate(total=Sum('amount'))['total'] or 0

    return float(received - sent)