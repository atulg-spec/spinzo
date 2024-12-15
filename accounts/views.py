import json
from .models import *
from django.http import JsonResponse
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

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
            return render(request, 'home/login.html', {'error': 'Invalid credentials'})
    return render(request, 'home/login.html')

