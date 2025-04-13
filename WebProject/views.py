from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def root(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')
