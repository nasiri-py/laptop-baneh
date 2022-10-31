from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets[0][1]["fields"] = ("phone_number", "username", "password"),
    UserAdmin.add_fieldsets[0][1]["fields"] = ("phone_number", "username", "password1", "password2"),

