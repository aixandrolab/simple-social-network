# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from chats.models import Chat, ChatStatus


@login_required()
def restore_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
        messages.error(request, 'You are not allowed to restore this chat')
        return redirect('chats:deleted_chats')
    chat_status = ChatStatus.objects.get(
        chat=chat,
        profile=request.user.profile,
    )
    if not chat_status.is_deleted:
        messages.error(request, 'Chat is not deleted!')
        return redirect('chats:active_chats')
    chat_status.is_deleted = False
    chat_status.save()
    messages.success(request, 'Chat was restored successfully')
    return redirect('chats:active_chats')
