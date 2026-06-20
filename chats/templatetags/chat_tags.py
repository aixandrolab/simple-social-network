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
def get_unread_messages_count(profile_id):
    return ChatStatus.objects.filter(
        profile__id=profile_id,
        is_muted=False,
        is_deleted=False,
        is_archived=False,
    ).filter(
        Q(chat__messages__is_read=False) &
        ~Q(chat__messages__sender__id=profile_id),
    ).count()


@register.simple_tag
def check_unread_messages(profile_id, chat_id):
    return ChatStatus.objects.filter(
        chat__id=chat_id,
        profile__id=profile_id,
        is_muted=False
    ).filter(
        Q(chat__messages__is_read=False) &
        ~Q(chat__messages__sender__id=profile_id)
    ).exists()


@register.simple_tag
def check_chat_status(profile_id, chat_id, status):
    chat_status = ChatStatus.objects.get(
        chat_id=chat_id,
        profile_id=profile_id,
    )

    if status == 'archived':
        archived_status = chat_status.is_archived
        return archived_status

    elif status == 'deleted':
        deleted_status = chat_status.is_deleted
        return deleted_status

    elif status == 'muted':
        muted_status = chat_status.is_muted
        return muted_status

    else:
        return "We don't know this status..."
