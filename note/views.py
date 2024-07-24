from django.shortcuts import render,get_object_or_404,redirect
from .models import Note
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.db import IntegrityError

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                backend = 'note.backends.CustomAuthBackend'
                user = authenticate(username=user.username, password=form.cleaned_data['password1'], backend=backend)
                if user is not None:
                    login(request, user, backend=backend)
                    return redirect('home')
                else:
                    messages.error(request, 'There was an error logging in. Please try again.')
            except IntegrityError:
                messages.error(request, 'This username is already taken. Please choose another.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'Your account has been deactivated.')
                    print(f"User {username} attempted to log in but is deactivated.")
            else:
                # Handle case where user is None after authentication
                if request.session.pop('deactivated_account', False):
                    messages.error(request, 'Your account has been deactivated.')
                    print(f"Deactivated user {username} attempted to log in.")
                else:
                    # Include additional debugging information
                    messages.error(request, 'Invalid username or password.')
                    print("Invalid username or password.")
        else:
            # Include additional debugging information for form errors
            print("Form errors:", form.errors)
            messages.error(request,'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def deactivate_account(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deactivated.")
        return redirect('login')
    else:
        messages.error(request, "You need to log in first.")
        return redirect('login')

@login_required
def index(request):
    notes=Note.objects.all()
    return render(request,'note/index.html',{'notes':notes})

@login_required
def detail(request,id):
    note=get_object_or_404(Note, id=id)
    return render(request,'note/detail.html',{'note':note})

@login_required
def create(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        Note.objects.create(title=title, content=content, user=request.user)
        return redirect('index')
    return render(request,'note/form.html')

@login_required
def update(request,id):
    note=get_object_or_404(Note, id=id)
    if request.method=='POST':
        note.title=request.POST.get('title')
        note.content=request.POST.get('content')
        note.save()
        return redirect('detail', id=id)
    return render(request,'note/form.html',{'note':note})

@login_required
def delete(request,id):
    note=get_object_or_404(Note, id=id)
    if request.method=='POST':
        note.delete()
        return redirect('index')
    return render(request,'note/confirm_delete.html',{'note':note})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')




