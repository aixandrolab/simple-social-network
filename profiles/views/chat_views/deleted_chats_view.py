from django.db.models import Q
from django.shortcuts import render

from core.utils.paginator import CachedCountPaginator
from profiles.models import Chat


def deleted_chats_view(request):
    profile = request.user.profile
    deleted_chats = (Chat.objects.select_related(
        'user1',
        'user1__user',
        'user2',
        'user2__user'
    )
    .filter(
        Q(user1_id=profile.id) | Q(user2_id=profile.id),
        chat_statuses__is_archived=False,
        chat_statuses__is_deleted=True,
        chat_statuses__is_muted=False,
        chat_statuses__is_visible=True,
        chat_statuses__profile_id=profile.id,
    ))
    deleted_chats_count = deleted_chats.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(deleted_chats, 10, total_count=deleted_chats_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'deleted_chats_count': deleted_chats_count,
        'profile': profile,
    }
    return render(request, 'profiles/chat_templates/deleted_chats.html', context)
