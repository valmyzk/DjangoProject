from django.urls  import path
from . import views

urlpatterns = [
    path('assets/', views.all_assets),
    path('asset/<str:symbol>', views.asset),
    path('asset/<str:symbol>/price', views.asset_price),
    path('holdings', views.holdings)
]