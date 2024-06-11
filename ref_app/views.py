from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.utils import html
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
# from django.views.decorators.cache import never_cache

from .forms import RegistrationForm
# BuyThingForm
from .models import Profile, Referral
from ref_app import data_app, utils


# Create your views here.
def create_ref_link(ref_code):
    domain = 'localhost'
    return f'http://{domain}:8000{reverse(data_app.REG_PATH)}?ref={ref_code}'

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

def logout_view(request):
    if not request.method == 'GET':
        return redirect(data_app.HOME_PATH)
    logout(request)
    return redirect(data_app.LOGIN_PATH)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ref_code = form.cleaned_data['ref_code']
            err, resp = utils.create_user((username, password, ref_code))
            if err:
                return redirect(data_app.LOGIN_PATH)
            user = authenticate(username=username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('profile')
    else:
        ref = request.GET.get('ref', '')
        form = RegistrationForm()
        form.fields['ref_code'].initial = ref
    return render(request, 'register.html', {'form': form})

def profile(request):
    if not request.method == 'GET':
        return redirect(data_app.HOME_PATH)
    err, ref_code = utils.get_ref_code(request.user)
    ref_link = create_ref_link(ref_code)
    return render(request, 'profile.html', {'ref_link': ref_link})

def store_view(request):
    if not request.method == 'GET':
        return redirect(data_app.HOME_PATH)
    err, balance = utils.get_balance_by_user(request.user)
    return render(request, 'store.html', {'products': data_app.PRODUCTS, 'balance': balance})

def post_buy_view(request):
    if request.method != "POST":
        return redirect(data_app.HOME_PATH)
    str_id = request.POST.get('product_id', '')
    if str_id:
        _id = int(str_id)
        if _id in [1, 2, 3]:
            err, resp = utils.buy_item_by_id(request.user, _id)
        else:
            print('not this id')
    else:
        print('product_id is empty')
    return redirect(data_app.HOME_PATH)

def give_money_view(request):
    s, resp1 = utils.get_money(request.user)
    return redirect(data_app.STORE_PATH)

def all_refs_view(request):
    err, refs = utils.get_all_referals()
    if err:
        return redirect(data_app.HOME_PATH)
    return render(request, 'all_refs.html', {'all_refs': refs})

def my_refs_view(request):
    err, refs = utils.get_referals_by_user(request.user)
    if err:
        return redirect(data_app.HOME_PATH)
    return render(request, 'my_refs.html', {'my_refs': refs})