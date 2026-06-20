# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from profiles.forms.disable_two_factor_form import Disable2FAForm


@login_required()
@require_http_methods(['GET', 'POST'])
def two_factor_disable_view(request):
    user = request.user

    if not user.profile.is_2fa_active:
        messages.warning(request, '2FA is not enabled for your account.')
        return redirect('profiles:two_factor_setup')

    if request.method == 'POST':
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            user.profile.disable_2fa()
            messages.success(request, '2FA has been disabled for your account.')
            return redirect('profiles:profile_detail', slug=user.profile.slug)
    else:
        form = Disable2FAForm(user)

    context = {
        'form': form
    }
    return render(request, 'profiles/two_factor_templates/two_factor_disable.html', context)
