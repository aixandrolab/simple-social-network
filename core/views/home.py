# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.shortcuts import render

from profiles.models import Profile


def home_view(request):
    last_registered_profile = Profile.objects.first()
    total_users = Profile.objects.filter(is_active=True).count()
    context = {
        'last_registered_profile': last_registered_profile,
        'total_users': total_users,
    }
    return render(request, 'core/index.html', context)
