from django.urls import path
from . import views

urlpatterns = [
    # Assets API
    path('assets/', views.all_assets, name='all_assets'),
    path('asset/<str:symbol>/', views.asset, name='asset'),
    path('asset/<str:symbol>/price/', views.asset_price, name='asset_price'),

    # Holdings (API y legacy)
    path('holdings/', views.holdings_api, name='holdings_api'),
    path('holdings-legacy/', views.holdings, name='holdings_legacy'),

    # Portfolio dashboard endpoints
    path('portfolio-history/', views.portfolio_history_api, name='portfolio_history_api'),
    path('portfolio-metrics/', views.portfolio_metrics_api, name='portfolio_metrics_api'),
]
