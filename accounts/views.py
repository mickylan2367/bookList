from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm

class SignupView(CreateView):
    model = User
    form_class = SignupForm #CreateViewで使うモデルを定義する（指定がなければ自動生成）
    template_name = 'accounts/signup.html'
    success_url =reverse_lazy('index')
