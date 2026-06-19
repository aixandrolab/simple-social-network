from django.db.models import Q
from django.template.defaulttags import register

from chats.models import Chat, ChatStatus


@register.simple_tag
def active_chats_count(profile):
    return Chat.objects.filter(
        Q(user1=profile) | Q(user2=profile),
        chat_statuses__is_archived=False,
        chat_statuses__is_deleted=False,
        chat_statuses__is_muted=False,
        chat_statuses__is_visible=True,
        chat_statuses__profile=profile,
    ).count()

@register.simple_tag
def archived_chats_count(profile):
    return Chat.objects.filter(
        Q(user1=profile) | Q(user2=profile),
        chat_statuses__is_archived=True,
        chat_statuses__is_deleted=False,
        chat_statuses__is_muted=False,
        chat_statuses__is_visible=True,
        chat_statuses__profile=profile,
    ).count()

@register.simple_tag
def deleted_chats_count(profile):
    return Chat.objects.filter(
        Q(user1=profile) | Q(user2=profile),
        chat_statuses__is_archived=False,
        chat_statuses__is_deleted=True,
        chat_statuses__is_muted=False,
        chat_statuses__is_visible=True,
        chat_statuses__profile=profile,
    ).count()

@register.simple_tag
def check_unread_messages(profile):
    chats = ChatStatus.objects.filter(
        profile=profile,
        is_muted=False
    ).filter(
        Q(chat__messages__is_read=False) &
        ~Q(chat__messages__sender=profile)
    ).count()
    return chats
