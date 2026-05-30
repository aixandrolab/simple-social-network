from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse

from core.services.email_service import Email
from profiles.models import PasswordResetToken


def resend_forgot_password_view(request):
    try:
        email = cache.get('resend_forgot_password')
        user = User.objects.get(email=email)
        token = PasswordResetToken.create_token(user)
        url = request.build_absolute_uri(
            reverse('core:reset_password', kwargs={'token': token.token})
        )
        Email.reset_password(user.email, url, user.username)
        messages.success(request, 'Email was successfully sent! Check your email for the envelope.')
    except Exception as e:
        messages.error(request, 'Please enter email again.')
    return redirect('core:forgot_password')
