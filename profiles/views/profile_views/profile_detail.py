from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.models.profile_model import Profile
from friends.services import FriendshipService


@login_required()
def profile_detail_view(request, slug):
    profile = Profile.objects.select_related('user').get(slug=slug)

    if request.user.profile != profile:
        friendship = FriendshipService.get_friendship(request.user.profile, profile)
    else:
        friendship = None

    friends_requests = FriendshipService.get_incoming_requests(request.user.profile)
    friends_requests_count = FriendshipService.get_incoming_requests_count(request.user.profile)

    context = {
        'profile': profile,
        'friendship': friendship,
        'friends_requests': friends_requests,
        'friends_requests_count': friends_requests_count,
    }
    return render(request, 'profiles/profile_detail.html', context)
