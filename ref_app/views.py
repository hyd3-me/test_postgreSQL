from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.utils import html
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
# from django.views.decorators.cache import never_cache

# from .forms import RegistrationForm, BuyThingForm
from .models import Profile, Referral
from ref_app import data_app, utils

# Create your views here.

def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')

def login_view(request):
    if not request.method == 'GET':
        if not request.method == 'POST':
            return redirect(data_app.HOME_PATH)
        form1 = AuthenticationForm(request, data=request.POST)
        if form1.is_valid():
            user1 = form1.get_user()
            login(request, user1)
            # messages.success(request, f'{test_data.SUCCESS_LOG}')
            return redirect(data_app.PROFILE_PATH)
        # messages.error(request, f'form invalid. perhaps there is no such user')
    else:
        form1 = AuthenticationForm()
    return render(request, 'login.html', {'form': form1})