# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from profiles.models.profile_model import Profile


@login_required()
def profile_search_view(request):
    profile_list = Profile.objects.select_related('user').all()
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            profile_list = Profile.objects.select_related('user').filter(
                Q(user__username__icontains=prompt) |
                Q(user__first_name__icontains=prompt)
            )
    context = {
        'profile_list': profile_list,
    }
    return render(request, 'profiles/profile_search.html', context)
