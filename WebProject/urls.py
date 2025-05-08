from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('assets/buy/', views.buy, name='buy'),
    path('assets/sell/', views.sell, name='sell'),
    path('funds/add/', views.add_funds, name='add_funds'),
    path('funds/withdraw/', views.transfer_funds, name='transfer_funds'),
    path('profile', views.my_profile, name='my_profile')
]
