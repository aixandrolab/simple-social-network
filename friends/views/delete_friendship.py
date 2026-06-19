from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from profiles.models import Profile
from friends.models.friendship_models import FriendshipStatus
from friends.services import FriendshipService


@login_required()
def delete_friendship_view(request, user_id):
    friend = Profile.objects.get(user__id=user_id)
    friendship = FriendshipService.get_friendship(request.user.profile, friend)
    if not friendship or friendship.status == FriendshipStatus.PENDING:
        messages.error(request, 'You are not friends with this user.')
        return redirect('friends:friends_list', request.user.username)

    try:
        FriendshipService.remove_friend(friendship, request.user.profile)
        messages.success(request, 'Friend removed successfully.')
    except ValidationError as e:
        messages.error(request, 'Something went wrong.')
        print(e)
    return redirect('friends:friends_list', request.user.username)
