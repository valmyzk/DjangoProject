from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('wallet/', views.wallet, name='wallet'),
    path('cash/', views.cash, name='cash'),
    path('assets/buy/', views.buy, name='buy'),
    path('assets/sell/', views.sell, name='sell'),
    path('funds/add/', views.add_funds, name='add_funds'),
    path('funds/transfer/', views.transfer_funds, name='transfer_funds'),
    path('profile', views.my_profile, name='my_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
]
