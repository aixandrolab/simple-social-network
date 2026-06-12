from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from core.utils.paginator import CachedCountPaginator
from profiles.models import Chat, ChatMessage


@login_required()
def active_chats_view(request):
    active_chat_list = Chat.objects.filter(
        Q(user1=request.user.profile) | Q(user2=request.user.profile),
        chat_statuses__is_archived=False,
        chat_statuses__is_deleted=False,
        chat_statuses__is_muted=False,
        chat_statuses__is_visible=True,
        chat_statuses__profile=request.user.profile,
    ).select_related(
        'user1',
        'user1__user',
        'user2',
        'user2__user'
    )
    active_chat_list_count = active_chat_list.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(active_chat_list, 10, total_count=active_chat_list_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'active_chat_list_count': active_chat_list_count,
    }
    return render(request, 'profiles/chat_templates/active_chats.html', context)
