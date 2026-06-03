from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models.profile_model import Profile
from profiles.services import FriendshipService


@login_required()
def profile_detail_view(request, slug):
    profile = Profile.objects.select_related('user').get(slug=slug)

    if request.user.profile != profile:
        friendship = FriendshipService.get_friendship(request.user.profile, profile)
    else:
        friendship = None

    context = {
        'profile': profile,
        'friendship': friendship,
    }
    return render(request, 'profiles/profile_detail.html', context)
