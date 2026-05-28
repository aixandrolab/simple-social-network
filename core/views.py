from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from core.forms.login_form import LoginForm
from core.forms.register_form import RegisterForm


def home_view(request):
    context = {

    }
    return render(request, 'core/index.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profiles:profile_detail')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Incorrect username or password fields!")
                return render(request, 'core/auth/login.html', {'form': form})

            login(request, user)
            messages.success(request, f"Welcome, {request.user.username}!")
            return redirect('profiles:profile_detail')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'core/auth/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid:
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                messages.success(request, "User is successfully created!")
                return redirect('core:login')

        except Exception as e:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'core/auth/register.html', {'form': form})
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'core/auth/register.html', context)