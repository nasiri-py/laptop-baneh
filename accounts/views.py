from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import generic
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'


class Logout(LogoutView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.next_page = request.GET.get('next')
