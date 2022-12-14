from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'username', 'password1', 'password2']

    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     user_ph = get_user_model().objects.filter(phone_number=phone_number).exists()
    #     if user_ph:
    #         raise ValidationError('User with this Phone Number already exists. Please enter other Phone Number')

    # def clean_username(self):
    #     username = self.data['username']
    #     user_us = get_user_model().objects.filter(username=username).exists()
    #     if user_us:
    #         raise ValidationError('User with this Username already exists. Please enter other Username')


class OtpCodeLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['phone_number'].disabled = True
            self.fields['username'].disabled = True

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'username', 'first_name', 'last_name']
