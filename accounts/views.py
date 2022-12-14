from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from .models import User
from django.views import generic, View
from .forms import RegisterForm, OtpCodeLoginForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from utils import send_sms, send_otp_code
from .models import OtpCode
from django.contrib import messages
from datetime import datetime, timedelta
import pytz
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from orders.models import Order
from products.models import Comment


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
            messages.success(self.request, f'کد تائید به شماره {cd["phone_number"]} ارسال شد', 'success')
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
            messages.error(self.request, 'شما در سایت ثبت نام نکرده اید', 'danger')
            return redirect('accounts:register')

    def form_valid(self, form):
        try:
            code_instance = OtpCode.objects.get(phone_number=self.user_session['phone_number'])
            if code_instance.created + timedelta(minutes=2) < datetime.now(tz=pytz.timezone('Asia/Tehran')):
                code_instance.delete()
                messages.error(self.request, 'کد وار شده منقضی شده است', 'danger')
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
                        messages.success(self.request, f'شما با موفقیت وارد شدید', 'success')
                        return redirect('home:home')
        except Exception:
            messages.error(self.request, 'کد وار شده منقضی شده است', 'danger')
            return redirect('accounts:verify')


class ResendCodeView(View):
    def get(self, request):
        user_session = request.session['user_registration']
        send_otp_code(user_session['phone_number'])
        messages.success(self.request, f'کد تائید به شماره {user_session["phone_number"]} ارسال شد', 'success')
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
                messages.success(self.request, f'کد تائید به شماره {cd["phone_number"]} ارسال شد', 'success')
                return redirect('accounts:verify')
            except User.DoesNotExist:
                messages.error(self.request, f"کاربری با شماره موبایل {cd['phone_number']} وجود ندارد", 'danger')
                return redirect('accounts:otp-code-login')


class PasswordResetView(View):
    form_class = OtpCodeLoginForm
    token_generator = PasswordResetTokenGenerator

    def get(self, request):
        form = self.form_class()
        return render(request, 'registration/password_reset.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                messages.error(self.request, f"کاربری با شماره موبایل {phone_number} وجود ندارد", 'danger')
                return redirect('accounts:password-reset')
            current_site = get_current_site(self.request)
            token_generator = self.token_generator()
            message = render_to_string('registration/password_reset_sms.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            print(message)
            send_sms(phone_number, message)
            request.session['password_reset'] = {
                'phone_number': phone_number,
            }
            messages.success(request, f'لینک بازیابی گذر واژه به شماره موبایل {phone_number} ارسال شد', 'success')
            return redirect('accounts:login')
        return redirect('home:home')


class PasswordResetConfirm(PasswordResetConfirmView):
    def get_success_url(self):
        messages.success(self.request, 'گذر واژه شما با موفقیت تغییر یافت', 'success')
        return reverse('accounts:login')


class Profile(LoginRequiredMixin, generic.UpdateView):
    template_name = 'registration/profile.html'
    form_class = ProfileForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.password_change_form = PasswordChangeForm

    def get_success_url(self):
        messages.success(self.request, 'تغییرات با موفقیت اعمال شد', 'success')
        return reverse("accounts:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_change_form'] = self.password_change_form(user=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:profile')


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'registration/comment_delete.html'
    success_url = reverse_lazy('accounts:profile')
