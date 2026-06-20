# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect

from friends.models.friendship_models import Friendship
from friends.services import FriendshipService


@login_required()
def cancel_friendship_request_view(request, friendship_id):
    friendship = get_object_or_404(Friendship, pk=friendship_id)
    try:
        FriendshipService.cancel_request(friendship, request.user.profile)
        messages.success(request, 'Friendship was cancelled successfully')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('profiles:profile_detail', slug=friendship.receiver.slug)
