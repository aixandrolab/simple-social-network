from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from profiles.forms.change_password_form import UserPasswordChangeForm
from profiles.forms.settings_form import SettingsForm
from profiles.models import Profile


@login_required()
def profile_detail_view(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile_detail.html', context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required()
def settings_view(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=user_profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile was successfully updated!')
            return redirect('profiles:profile_detail')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'profiles/settings.html', {'form': form})
    else:
        form = SettingsForm(instance=user_profile)
    context = {
        'form': form
    }
    return render(request, 'profiles/settings/settings.html', context)


@login_required()
def change_password_view(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile password was successfully updated!')
            return redirect('profiles:profile_detail')
        else:
            messages.error(request, 'Incorrect input!')
    else:
        form = UserPasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'profiles/settings/change_password.html', context)
