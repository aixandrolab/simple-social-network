from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from profiles.forms.settings_form import SettingsForm
from profiles.models import Profile


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
    return render(request, 'profiles/settings_templates/settings.html', context)
