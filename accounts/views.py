import json
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def index(request):
    return render(request, 'landing/home.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/')

def register(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.get_full_path() == '/register':
        superuser = CustomUser.objects.filter(is_superuser=True).first()
        return redirect(f'/register?referral_code={superuser.referral_code}')
    referral_code = request.GET.get('referral_code', None)
    referrer = None
    
    if referral_code:
        referrer = get_object_or_404(CustomUser, referral_code=referral_code)
    else:
        messages.error(request, 'Invalid Referral URL !')
        superuser = CustomUser.objects.filter(is_superuser=True).first()
        return redirect(f'/register?referral_code={superuser.referral_code}')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if referrer:
                user.user_invited_by = referrer
            user.save()

            if referrer:
                referrer.team_members.add(user)

            login(request, user)
            return redirect('/home')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()

    return render(request, 'landing/register.html', {
        'form': form,
        'referral_code': referral_code,
    })



def handlelogin(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Logged In Successfully')
            return redirect('/home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'landing/login.html', {'error': 'Invalid credentials'})
    return render(request, 'landing/login.html')

