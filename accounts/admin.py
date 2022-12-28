from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OtpCode

admin.site.site_header = 'استوک لپ تاپ استور'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'phone_number', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'phone_number', 'first_name', 'last_name']
    UserAdmin.fieldsets[0][1]["fields"] = ("phone_number", "username", "password"),
    UserAdmin.add_fieldsets[0][1]["fields"] = ("phone_number", "username", "password1", "password2"),


admin.site.register(OtpCode)

