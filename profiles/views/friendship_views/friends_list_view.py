from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.utils.paginator import CachedCountPaginator
from profiles.models import Profile
from profiles.services import FriendshipService


@login_required()
def friends_list_view(request, username):
    target_user = request.user.profile if username == request.user.username else get_object_or_404(
        Profile,
        user__username=username
    )
    friends = FriendshipService.get_friends(target_user)
    friends_count = FriendshipService.get_friends_count(target_user)
    if target_user.user.username == request.user.username:
        incoming_count = FriendshipService.get_incoming_requests_count(request.user.profile)
        outgoing_count = FriendshipService.get_outgoing_requests_count(request.user.profile)
    else:
        incoming_count = 0
        outgoing_count = 0
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(friends, 10, total_count=friends_count)
    page_obj = paginator.get_page(page)

    context = {
        'target_user': target_user,
        'friends_count': friends_count,
        'page_obj': page_obj,
        'incoming_count': incoming_count,
        'outgoing_count': outgoing_count,
    }
    return render(request, 'profiles/friends_list.html', context)
