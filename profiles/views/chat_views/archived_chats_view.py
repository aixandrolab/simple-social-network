from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from core.utils.paginator import CachedCountPaginator
from profiles.models import Chat


@login_required()
def archived_chats_view(request):
    archived_chats = Chat.objects.filter(
        Q(user1=request.user.profile) | Q(user2=request.user.profile),
        chat_statuses__is_archived = True,
        chat_statuses__is_deleted = False,
        chat_statuses__is_muted = False,
        chat_statuses__is_visible = True,
        chat_statuses__profile = request.user.profile,
    )
    archived_chats_count = archived_chats.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(archived_chats, 10, total_count=archived_chats_count)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'archived_chats_count': archived_chats_count,
    }
    return render(request, 'profiles/chat_templates/archived_chats.html', context)
