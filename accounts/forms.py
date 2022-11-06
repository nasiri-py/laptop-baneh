from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'username', 'password1', 'password2']


class OtpCodeLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
