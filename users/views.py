from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class LoginUserView(LoginView):
    success_url = reverse_lazy('/')
    template_name = 'users/login.html'
    redirect_authenticated_user = True
