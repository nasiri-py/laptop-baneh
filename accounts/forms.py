from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'username', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if str(phone_number[:2]) != '09' or len(phone_number) != 11:
            raise ValidationError('فرمت شماره موبایل صحیح نمیباشد.')
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            raise ValidationError('کاربری با آن شماره موبایل وجود دارد.')
        return phone_number


class OtpCodeLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['username'].disabled = True

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'username', 'first_name', 'last_name']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if str(phone_number[:2]) != '09' or len(phone_number) != 11:
            raise ValidationError('فرمت شماره موبایل صحیح نمیباشد.')
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            raise ValidationError('کاربری با آن شماره موبایل وجود دارد.')
        return phone_number
