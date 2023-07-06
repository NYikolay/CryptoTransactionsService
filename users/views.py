from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from users.decorators import redirect_authenticated_user


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    @redirect_authenticated_user
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LoginUserView(LoginView):
    success_url = reverse_lazy('transactions:transactions')
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'login'

    def get(self, request):
        logout(request)
        return redirect('users:login')
