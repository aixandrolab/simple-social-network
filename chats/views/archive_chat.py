from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from chats.models import ChatStatus, Chat


@login_required
def archive_chat_view(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
        if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
            messages.error(request, 'You cannot archive this chat')
            return redirect('chats:active_chats')
        chat_status = ChatStatus.objects.get(chat=chat, profile=request.user.profile)
        if chat_status.is_archived:
            messages.error(request, 'You cannot archive this chat')
            return redirect('chats:archived_chats')
        chat_status.is_archived = True
        chat_status.save()
        messages.success(request, 'Chat was archived successfully')
        return redirect('chats:archived_chats')
    except Exception as e:
        messages.error(request, f'Chat does not exist!')
        print(e)
        return redirect('chats:active_chats')
