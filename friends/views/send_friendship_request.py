# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect

from profiles.models import Profile
from friends.models.friendship_models import FriendshipStatus
from friends.services import FriendshipService


@login_required()
def send_friendship_request_view(request, user_id):
    receiver = get_object_or_404(Profile, user_id=user_id)
    try:
        friendship = FriendshipService.send_friendship_request(request.user.profile, receiver)
        if friendship.status == FriendshipStatus.ACCEPTED:
            msg = f"You and {receiver.user.username} are now friends."
            messages.success(request, msg)
        else:
            messages.success(request, f'Friendship request successfully sent.')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect(receiver.get_absolute_url())
