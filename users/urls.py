from django.contrib import admin
from django.urls import path

from users.views import SignUpView, LoginUserView

app_name = 'users'

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login')
]
