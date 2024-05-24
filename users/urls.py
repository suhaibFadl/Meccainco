from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register
from .forms import CustomLoginForm

app_name = 'users'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
]