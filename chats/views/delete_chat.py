# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from chats.models import Chat, ChatStatus


@login_required()
def delete_chat_view(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
        messages.error(request, "You can't delete other users' chats!")
        return redirect('chats:active_chats')
    chat_status = ChatStatus.objects.get(chat_id=chat_id, profile=request.user.profile)
    if chat_status.is_deleted:
        messages.error(request, "Chat is already deleted!")
        return redirect('chats:deleted_chats')
    if chat_status.is_archived:
        chat_status.is_archived = False
    chat_status.is_deleted = True
    chat_status.save()
    chat_status_user1 = ChatStatus.objects.get(chat_id=chat_id, profile=chat.user1)
    chat_status_user2 = ChatStatus.objects.get(chat_id=chat_id, profile=chat.user2)
    if chat_status_user1.is_deleted and chat_status_user2.is_deleted:
        chat.delete()
    messages.success(request, "Successfully deleted chat!")
    return redirect('chats:deleted_chats')
