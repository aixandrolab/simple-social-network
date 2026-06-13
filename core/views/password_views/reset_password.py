from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from core.forms.reset_password import ResetPasswordForm
from profiles.models.password_reset_token_model import PasswordResetToken


@never_cache
def reset_password_view(request, token):
    cache.delete('resend_forgot_password')

    token = get_object_or_404(PasswordResetToken, token=token)

    user = token.user

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'core/password_templates/reset_password.html', {'form': form})
            user.set_password(new_password)
            user.save()
            token.use_token()
            messages.success(request, 'Congratulations! Your password is updated!'
                                    ' Now, login with your new password.')
            return redirect('core:login')
    else:
        form = ResetPasswordForm()

    context = {
        'form': form
    }
    return render(request, 'core/password_templates/reset_password.html', context)
