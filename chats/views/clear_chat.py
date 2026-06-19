from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from chats.models import Chat, ChatMessage


@login_required()
def clear_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
        messages.error(request, "You're not participant of this chat")
        return redirect('chats:active_chats')
    ChatMessage.objects.filter(chat=chat).delete()
    messages.success(request, f'Chat successfully cleared.')
    return redirect('chats:chat_detail', chat_id)
