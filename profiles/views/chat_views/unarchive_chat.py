from django.contrib import messages
from django.shortcuts import redirect

from profiles.models import Chat, ChatStatus


def unarchive_chat_view(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
        if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
            messages.error(request, 'You cannot unarchive this chat')
            return redirect('profiles:archived_chats')
        chat_status = ChatStatus.objects.get(chat=chat, profile=request.user.profile)
        if not chat_status.is_archived:
            messages.error(request, 'You cannot unarchive this chat')
            return redirect('profiles:active_chats')
        chat_status.is_archived = False
        chat_status.save()
        messages.success(request, 'Chat was unarchived successfully')
        return redirect('profiles:active_chats')
    except Exception as e:
        messages.error(request, f'Chat does not exist!')
        return redirect('profiles:archived_chats')
