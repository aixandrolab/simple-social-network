from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from core.forms.login_form import LoginForm
from profiles.models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profiles:profile_detail', slug=request.user.profile.slug)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']


            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Incorrect username or password fields!")
                return render(request, 'core/auth/login.html', {'form': form})

            if not user.profile.is_email_verified:
                messages.info(request, "Your account is not activated! Please check your email"
                                       " for verification envelope")
                return render(request, 'core/auth/login.html', {'form': form})

            if user.profile.is_2fa_active:
                request.session['2fa_user_id'] = user.id
                messages.info(request, 'Please complete two-factor authentication.')
                return redirect('profiles:two_factor_verify')

            login(request, user)
            messages.success(request, f"Welcome, {request.user.username}!")
            return redirect('profiles:profile_detail', slug=user.profile.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'core/auth/login.html', context)
