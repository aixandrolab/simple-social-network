from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from chats.forms.chat_settings_form import ChatSettingsForm
from chats.models import Chat, ChatStatus


@login_required()
def chat_settings_view(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    chat_status = ChatStatus.objects.get(chat=chat, profile=request.user.profile)

    if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
        messages.error(request, "You can't update this chat.")
        return redirect('chats:active_chats')

    if request.method == 'POST':
        form = ChatSettingsForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chat name changed successfully')
            return redirect('chats:chat_detail', chat_id)
    else:
        form = ChatSettingsForm(instance=chat)

    context = {
        'chat': chat,
        'form': form,
        'chat_status': chat_status,
    }

    return render(request, 'chats/chat_settings.html', context)
