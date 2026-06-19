from django.shortcuts import render

from core.utils.paginator import CachedCountPaginator
from friends.services import FriendshipService


def outgoing_friendship_requests_view(request):
    requests_list = FriendshipService.get_outgoing_requests(request.user.profile)
    requests_count = FriendshipService.get_outgoing_requests_count(request.user.profile)
    friends_count = FriendshipService.get_friends_count(request.user.profile)
    incoming_count = FriendshipService.get_incoming_requests_count(request.user.profile)
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(requests_list, 10, total_count=requests_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'requests_list': requests_list,
        'requests_count': requests_count,
        'incoming_count': incoming_count,
        'friends_count': friends_count,
    }
    return render(request, 'friends/outgoing_friendship_requests.html', context)
