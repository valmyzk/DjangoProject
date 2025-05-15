from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm

def signup(request: HttpRequest) -> HttpResponse:
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

@login_required
def my_profile(request: HttpRequest) -> HttpResponse:
    return render(request, 'profile/my_profile.html', {'user': request.user})

@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        pass_form = CustomPasswordChangeForm(request.user, request.POST)

        # Primer validem el formulari del perfil
        if form.is_valid():
            form.save()

            # Si algun camp de contrasenya s'ha omplert...
            old = request.POST.get('old_password')
            new1 = request.POST.get('new_password1')
            new2 = request.POST.get('new_password2')

            if old or new1 or new2:
                if pass_form.is_valid():
                    pass_form.save()
                    update_session_auth_hash(request, pass_form.user)
                else:
                    # Si hi ha errors a la contrasenya, es tornen a mostrar
                    return render(request, 'profile/edit_profile.html', {
                        'form': form,
                        'pass_form': pass_form
                    })

            return redirect('my_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
        pass_form = CustomPasswordChangeForm(request.user)

    return render(request, 'profile/edit_profile.html', {
        'form': form,
        'pass_form': pass_form
    })
