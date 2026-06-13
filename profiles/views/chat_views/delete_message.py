from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from profiles.models import Chat, ChatMessage


@login_required()
def delete_message_view(request, chat_id, message_id):
    chat = Chat.objects.get(id=chat_id)
    chat_message = ChatMessage.objects.get(id=message_id, chat=chat)
    if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
        messages.error(request, 'You are not allowed to delete messages')
        return redirect('profiles:active_chats')
    chat_message.delete()
    return redirect('profiles:chat_detail', chat_id)
