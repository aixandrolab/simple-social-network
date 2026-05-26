from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from core.forms import LoginForm


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
            print(user)

            if user is None:
                messages.error(request, "Incorrect username or password fields!")
                return render(request, 'core/auth/login.html', {'form': form})

            login(request, user)
            return redirect('profiles:profile_detail')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'core/auth/login.html', context)