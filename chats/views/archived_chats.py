from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from chats.models import Chat
from core.utils.paginator import CachedCountPaginator


@login_required()
def archived_chats_view(request):
    archived_chats = Chat.objects.filter(
        Q(user1=request.user.profile) | Q(user2=request.user.profile),
        chat_statuses__is_archived = True,
        chat_statuses__is_deleted = False,
        chat_statuses__is_visible = True,
        chat_statuses__profile = request.user.profile,
    ).select_related(
        'user1',
        'user1__user',
        'user2',
        'user2__user'
    )
    archived_chats_count = archived_chats.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(archived_chats, 10, total_count=archived_chats_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'archived_chats_count': archived_chats_count,
    }
    return render(request, 'chats/archived_chats.html', context)
