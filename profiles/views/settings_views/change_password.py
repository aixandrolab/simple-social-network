# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from profiles.forms.change_password_form import ChangePasswordForm


@login_required()
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile password was successfully updated!')
            return redirect('profiles:profile_detail', slug=request.user.profile.slug)
        else:
            messages.error(request, 'Incorrect input!')
    else:
        form = ChangePasswordForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'profiles/settings_templates/change_password.html', context)
