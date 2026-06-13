from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from django.views.decorators.cache import never_cache

from profiles.models.email_verification_token_model import EmailVerificationToken


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
