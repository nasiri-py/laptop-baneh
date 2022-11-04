from django.shortcuts import redirect
from .models import User
from django.views import generic, View
from .forms import RegisterForm, VerifyForm
from django.contrib.auth.views import LogoutView
import random
from utils import send_sms
from .models import OtpCode
from django.contrib import messages
from datetime import datetime, timedelta
import pytz


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        if form.is_valid():
            code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_sms(cd['phone_number'], f'{code}کد تایید شما به استوک لپ تاپ استور: ')
            OtpCode.objects.create(phone_number=cd['phone_number'], code=code)
            self.request.session['user_registration'] = {
                'phone_number': cd['phone_number'],
                'username': cd['username'],
                'password': cd['password1'],
            }
            print('='*100)
            print(code)
            # messages.success(self.request, f'کد تایید به شماره {cd["phone_number"]} ارسال شد.', 'success')
            return redirect('accounts:verify')


class VerifyView(generic.CreateView):
    model = OtpCode
    fields = ['code']
    template_name = 'registration/verify.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user_session = self.request.session['user_registration']
            return super().dispatch(request, *args, **kwargs)
        except Exception:
            # messages.error(self.request, 'You are not registered', 'danger')
            return redirect('accounts:register')

    def form_valid(self, form):
        try:
            code_instance = OtpCode.objects.get(phone_number=self.user_session['phone_number'])
            if code_instance.created + timedelta(minutes=2) < datetime.now(tz=pytz.timezone('Asia/Tehran')):
                code_instance.delete()
                # messages.error(self.request, 'This code is expired!', 'danger')
                return redirect('accounts:verify')
            if form.is_valid():
                cd = form.cleaned_data
                if cd['code'] == code_instance.code:
                    User.objects.create_user(self.user_session['phone_number'], self.user_session['username'],
                                             self.user_session['password'])
                    del self.user_session
        except Exception:
            # messages.error(self.request, 'This code is expired!', 'danger')
            return redirect('accounts:verify')
        return redirect('accounts:login')


class ResendCodeView(View):
    def get(self, request):
        code = random.randint(1000, 9999)
        user_session = request.session['user_registration']
        send_sms(user_session['phone_number'], f'Your verification code is {code}.')
        code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number'])
        if code_instance.exists():
            code_instance.delete()
        OtpCode.objects.create(phone_number=user_session['phone_number'], code=code)
        # messages.success(request, f"We send you a verification code to {user_session['phone_number']}.", 'success')
        return redirect('accounts:verify')


class Logout(LogoutView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_page = request.GET.get('next')
