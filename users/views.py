from django.shortcuts import render, redirect
from .forms import SignupForm


# Create your views here.
def registration(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'registration.html', {"form":form})