from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse

from core.forms.forgot_password import ForgotPasswordForm
from core.services.email_service import Email
from profiles.models.password_reset_token_model import PasswordResetToken


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                messages.success(request, 'Email was sent! Check your email for the letter.')
                print(e)
                return render(request, 'core/password_templates/forgot_password.html', {'form': form})

            token = PasswordResetToken.create_token(user)
            url = request.build_absolute_uri(
                    reverse('core:reset_password', kwargs={'token': token.token})
                )
            Email.reset_password(email, url, user.username)
            messages.success(request, 'Email was sent! Check your email for the letter.')
            cache.set(f'resend_forgot_password', email)
        else:
            messages.error(request, 'Please check that your email is correct.')
    else:
        form = ForgotPasswordForm()

    context = {
        'form': form,
    }
    return render(request, 'core/password_templates/forgot_password.html', context)
