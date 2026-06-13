from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from profiles.models import Chat, ChatMessage


@login_required()
def send_message_view(request, chat_id):
    if request.method == 'POST':
        chat = Chat.objects.get(id=chat_id)
        if request.user.profile != chat.user1 and request.user.profile != chat.user2:
            messages.error(request, 'You cannot send a message to this chat!')
            return redirect('profiles:active_chat')

        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(
                chat=chat,
                sender=request.user.profile,
                content=content,
            )
        else:
            messages.error(request, 'Messages cannot ve empty!')
    return redirect('profiles:chat_detail', chat_id)
