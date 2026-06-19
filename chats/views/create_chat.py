from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from chats.models import Chat, ChatStatus
from profiles.models import Profile


def create_chat_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    check_chat_exist = Chat.objects.filter(
        Q(user1=request.user.profile, user2=profile) | Q(user2=request.user.profile, user1=profile)
    )
    if check_chat_exist.exists() and check_chat_exist:
        return redirect('chats:chat_detail', check_chat_exist.first().pk)

    if request.method == 'POST':
        chat_name = request.POST.get('chat_name')

        chat = Chat.objects.create(
            name=chat_name,
            user1=request.user.profile,
            user2=profile,
        )
        chat.save()
        chat_status_user1 = ChatStatus.objects.create(
            chat=chat,
            profile=request.user.profile,
            is_visible=True,
        )
        chat_status_user2 = ChatStatus.objects.create(
            chat=chat,
            profile=profile,
            is_visible=True,
        )
        chat_status_user1.save()
        chat_status_user2.save()
        messages.success(request, 'Chat created successfully')
        return redirect('chats:chat_detail', chat.pk)

    context = {
        'profile': profile,
    }
    return render(request, 'chats/create_chat.html', context)
