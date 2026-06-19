from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect

from friends.models.friendship_models import Friendship
from friends.services import FriendshipService


@login_required()
def reject_friendship_request_view(request, friendship_id):
    friendship = get_object_or_404(Friendship, pk=friendship_id)
    try:
        FriendshipService.reject_request(friendship, request.user.profile)
        messages.success(request, 'Friendship rejected')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('friends:incoming_friendship_requests')
