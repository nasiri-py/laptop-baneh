from django.shortcuts import redirect, render
from .models import User
from django.views import generic, View
from .forms import RegisterForm, OtpCodeLoginForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
import random
from utils import send_sms, send_otp_code
from .models import OtpCode
from django.contrib import messages
from datetime import datetime, timedelta
import pytz


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        if form.is_valid():
            cd = form.cleaned_data
            send_otp_code(cd['phone_number'])
            self.request.session['user_registration'] = {
                'phone_number': cd['phone_number'],
                'username': cd['username'],
                'password': cd['password1'],
            }
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
            print(code_instance)
            if code_instance.created + timedelta(minutes=2) < datetime.now(tz=pytz.timezone('Asia/Tehran')):
                code_instance.delete()
                # messages.error(self.request, 'This code is expired!', 'danger')
                return redirect('accounts:verify')
            if form.is_valid():
                cd = form.cleaned_data
                if cd['code'] == code_instance.code:
                    if User.objects.filter(phone_number=self.user_session['phone_number']).exists():
                        user = User.objects.get(phone_number=self.user_session['phone_number'])
                    else:
                        user = User.objects.create_user(self.user_session['phone_number'],
                                                        self.user_session['username'],
                                                        self.user_session['password'])
                    del self.user_session
                    code_instance.delete()
                    if user is not None:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(self.request, user)
                        return redirect('accounts:profile')
        except Exception:
            # messages.error(self.request, 'This code is expired!', 'danger')
            return redirect('accounts:verify')


class ResendCodeView(View):
    def get(self, request):
        user_session = request.session['user_registration']
        send_otp_code(user_session['phone_number'])
        # messages.success(request, f"We send you a verification code to {user_session['phone_number']}.", 'success')
        return redirect('accounts:verify')


class OtpCodeLoginView(View):
    form_class = OtpCodeLoginForm
    template_name = 'registration/otp_code_login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                User.objects.get(phone_number=cd['phone_number'])
                send_otp_code(cd['phone_number'])
                request.session['user_registration'] = {
                    'phone_number': cd['phone_number'],
                }
                # messages.success(self.request, f"We send you a verification code to {cd['phone_number']}.", 'success')
                return redirect('accounts:verify')
            except User.DoesNotExist:
                # messages.error(self.request, f"User with this phone number does not exist.", 'danger')
                return redirect('accounts:otp-code-login')


class Logout(LogoutView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_page = request.GET.get('next')
