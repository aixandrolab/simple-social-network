from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from profiles.models import Chat, ChatMessage


def chat_detail_view(request, chat_id):
    chat = get_object_or_404(
        Chat.objects.select_related('user1', 'user2', 'user1__user', 'user2__user'),
        id=chat_id
    )
    if request.user.profile != chat.user1 and request.user.profile != chat.user2:
        messages.error(request, 'You are not authorized to view this chat')
        return redirect('profiles:active_chats')
    chat_messages = ChatMessage.objects.filter(chat=chat).prefetch_related('sender', 'sender__user')
    unread_messages = ChatMessage.objects.filter(
        ~Q(sender=request.user.profile),
        chat=chat,
        is_read=False
    )
    if unread_messages.exists():
        unread_messages.update(is_read=True)
    context = {
        'chat': chat,
        'chat_messages': chat_messages,
    }
    return render(request, 'profiles/chat_templates/chat_detail.html', context)
