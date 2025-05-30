from django.contrib.auth import update_session_auth_hash

from .forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import auth
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserChangeForm, OptionalPasswordChangeForm
from .forms import UserChangeForm, OptionalPasswordChangeForm
from django.contrib.auth import update_session_auth_hash



from .forms import UserCreationForm

def my_profile(request):
    return render(request, 'profile/my_profile.html')

def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth.login(request, form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('root')

import os
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import UserChangeForm, OptionalPasswordChangeForm


def edit_profile(request):
    user = request.user

    # Ruta completa a la carpeta d'avatars dins static/
    avatar_dir = os.path.join('static', 'img', 'avatars')
    avatar_choices = [f"img/avatars/{f}" for f in os.listdir(avatar_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        pass_form = OptionalPasswordChangeForm(user, request.POST)

        if form.is_valid() and pass_form.is_valid():
            updated_user = form.save(commit=False)

            # Assignar avatar seleccionat
            avatar_path = request.POST.get('avatar_path')
            if avatar_path:
                updated_user.avatar_path = avatar_path

            updated_user.save()

            if pass_form.is_filled():
                pass_form.save()
                update_session_auth_hash(request, pass_form.user)

            return redirect('my_profile')
    else:
        form = UserChangeForm(instance=user)
        pass_form = OptionalPasswordChangeForm(user)

    return render(request, 'profile/edit_profile.html', {
        'form': form,
        'pass_form': pass_form,
        'avatar_choices': avatar_choices
    })
