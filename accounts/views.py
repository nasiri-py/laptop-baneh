from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from .models import User
from django.views import generic, View
from .forms import RegisterForm, OtpCodeLoginForm, ProfileForm
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
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
from products.models import Comment
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash


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
                'url': self.request.path
            }
            messages.success(self.request, f'کد تائید به شماره {cd["phone_number"]} ارسال شد')
            return redirect('accounts:verify')
        return redirect('accounts:register')


class VerifyView(generic.CreateView):
    model = OtpCode
    fields = ['code']
    template_name = 'registration/verify.html'

    def get(self, request, *args, **kwargs):
        try:

            # user can be redirected here only from specific views (RegisterView, ResendCodeView, OtpCodeLoginView, Profile)
            user_session = request.session['user_registration']
            if user_session['url']:
                del user_session['url']
                request.session.modified = True
                return super().get(request, *args, **kwargs)
        except Exception:
            return redirect('accounts:login')

    def form_valid(self, form):
        user_session = self.request.session['user_registration']
        try:

            # check otp code time out
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
            if code_instance.created + timedelta(minutes=3) < datetime.now(tz=pytz.timezone('Asia/Tehran')):
                code_instance.delete()
                messages.error(self.request, 'کد وارد شده منقضی شده است. لطفا دوباره تلاش کنید')
                return redirect('accounts:login')

            if form.is_valid():
                cd = form.cleaned_data
                # check received code from user
                if int(cd['code']) == int(code_instance.code):
                    # for login by otp code
                    if User.objects.filter(phone_number=user_session['phone_number']).exists():
                        user = User.objects.get(phone_number=user_session['phone_number'])
                    # for change user number
                    elif user_session['phone_number_old']:
                        user = User.objects.get(phone_number=user_session['phone_number_old'])
                        user.phone_number = user_session['phone_number']
                        user.first_name = user_session['f_name']
                        user.last_name = user_session['l_name']
                        user.save()
                        messages.success(self.request, f'تغییرات به پروفایل شما اعمال شد')
                        return redirect('accounts:profile')
                    # for crate user
                    else:
                        user = User.objects.create_user(user_session['phone_number'],
                                                        user_session['username'],
                                                        user_session['password'])
                    del user_session
                    code_instance.delete()
                    if user is not None:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(self.request, user)
                        return redirect('home:home')
                return redirect('accounts:verify')
        except Exception:
            messages.error(self.request, 'کد وارد شده منقضی شده است. لطفا دوباره تلاش کنید')
            return redirect('accounts:login')


def verify_check_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        code = request.POST.get('code')
        qs = OtpCode.objects.filter(code__exact=code)
        if len(code) != 4:
            res = 'کد تائید باید 4 رقمی باشد'
        elif qs.exists():
            res = 'TrueAccess'
        else:
            res = 'کد وارد شده صحیح نمیباشد'
        return JsonResponse({'data': res})
    return JsonResponse({})


class ResendCodeView(View):
    def get(self, request):
        return redirect('accounts:login')

    def post(self, request):

        # user can request only by resend code form (input name = access)
        if request.POST['access']:
            user_session = self.request.session['user_registration']
            user_session['url'] = self.request.path
            self.request.session.modified = True
            send_otp_code(user_session['phone_number'])
            messages.success(self.request, f'کد تائید به شماره {user_session["phone_number"]} ارسال شد')
            return redirect('accounts:verify')
        return redirect('accounts:login')


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
                    'url': request.path
                }
                messages.success(self.request, f'کد تائید به شماره {cd["phone_number"]} ارسال شد')
                return redirect('accounts:verify')
            except User.DoesNotExist:
                messages.error(self.request, f"کاربری با شماره موبایل {cd['phone_number']} وجود ندارد")
                return redirect('accounts:otp-code-login')
        return render(request, self.template_name, {'form': form})


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
                messages.error(self.request, f"کاربری با شماره موبایل {phone_number} وجود ندارد")
                return redirect('accounts:password-reset')

            # send password reset address to user
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
            messages.success(request, f'لینک بازیابی گذرواژه به شماره موبایل {phone_number} ارسال شد')
            return redirect('accounts:login')
        return render(request, 'registration/password_reset.html', {'form': form})


class PasswordResetConfirm(PasswordResetConfirmView):
    def get_success_url(self):
        messages.success(self.request, 'گذرواژه شما با موفقیت تغییر یافت')
        return reverse('accounts:login')


class Profile(LoginRequiredMixin, generic.UpdateView):
    template_name = 'registration/profile.html'
    form_class = ProfileForm

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        # send user to kwargs
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            phone_number_new = form.cleaned_data['phone_number']
            phone_number_old = self.request.user.phone_number

            # if user change phone number, redirect to VerifyView
            if phone_number_new != phone_number_old:
                self.request.session['user_registration'] = {
                    'phone_number': phone_number_new,
                    'phone_number_old': phone_number_old,
                    'f_name': form.cleaned_data['first_name'],
                    'l_name': form.cleaned_data['last_name'],
                    'url': self.request.path,
                }
                send_otp_code(phone_number_new)
                messages.success(self.request, f'کد تائید به شماره {phone_number_new} ارسال شد')
                return redirect('accounts:verify')

            form.save()
            messages.success(self.request, 'تغییرات به پروفایل شما اعمال شد')
            return redirect('accounts:profile')
        return render(self.request, self.template_name, {'form': form})


class PasswordChange(LoginRequiredMixin, PasswordChangeView):

    def form_valid(self, form):
        form.save()

        # change password
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'گذرواژه شما تغییر کرد')
        return redirect('accounts:profile')


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'registration/comment_delete.html'
    success_url = reverse_lazy('accounts:profile')
