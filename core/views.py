from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache

from core.forms.login_form import LoginForm
from core.forms.register_form import RegisterForm
from core.services.email_service import Email
from profiles.models import EmailVerificationToken


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

            if not user.profile.is_email_verified:
                messages.info(request, "Your account is not activated! Please check your email"
                                       " for verification envelope")
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

                token = EmailVerificationToken.create_token(new_user)

                url = request.build_absolute_uri(
                    reverse('core:confirm_register', kwargs={'token': token.token})
                )

                Email.verification(new_user.email, url, new_user.username)
                messages.success(request,
                                 "User is successfully created!"
                                 " Now, you need to confirm your registration."
                                 " Please check your E-mail"
                                 )
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


@never_cache
def confirm_register_view(request, token):
    token = get_object_or_404(EmailVerificationToken, token=token)

    user = token.user

    if user.profile.is_email_verified:
        messages.info(request, 'Your account is already verified! You can login now.')

    user.profile.is_email_verified = True
    user.save()

    token.use_token()

    messages.success(request, "Congratulations! Your account is now verified! Now, login in your account.")
    return redirect('core:login')
