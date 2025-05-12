import django.contrib.auth.admin
from django.contrib import auth
from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm
from .models import User

class UserAdmin(auth.admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    list_display = ('email', 'is_staff')
    list_filter = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)