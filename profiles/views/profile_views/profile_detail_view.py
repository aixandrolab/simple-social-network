from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models import Profile


@login_required()
def profile_detail_view(request, slug):
    profile = Profile.objects.get(slug=slug)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/profile_detail.html', context)
