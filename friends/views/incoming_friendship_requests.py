from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.utils.paginator import CachedCountPaginator
from friends.services import FriendshipService


@login_required()
def incoming_friendship_requests_view(request):
    requests_list = FriendshipService.get_incoming_requests(request.user.profile)
    requests_count = FriendshipService.get_incoming_requests_count(request.user.profile)
    friends_count = FriendshipService.get_friends_count(request.user.profile)
    outgoing_count = FriendshipService.get_outgoing_requests_count(request.user.profile)
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(requests_list, 10, total_count=requests_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'requests_list': requests_list,
        'requests_count': requests_count,
        'outgoing_count': outgoing_count,
        'friends_count': friends_count,
    }
    return render(request, 'friends/incoming_friendship_requests.html', context)
