from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from profiles.models import Chat, ChatMessage


@login_required()
@require_http_methods(["POST"])
def edit_message_view(request, chat_id, message_id):
    try:
        chat = get_object_or_404(Chat, pk=chat_id)
        if chat.user1 != request.user.profile and chat.user2 != request.user.profile:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'You are not participant in this chat.'}, status=403)
            messages.error(request, 'You are not participant in this chat')
            return redirect('profiles:active_chats')

        message = get_object_or_404(ChatMessage, pk=message_id)
        if message.sender != request.user.profile:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'You can only edit your own messages'}, status=403)
            messages.error(request, 'You are allowed to edit this message.')
            return redirect('profiles:active_chats')

        edited_message = request.POST.get('content')
        if not edited_message:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Message cannot be empty!'}, status=400)
            messages.error(request, 'Message cannot be empty!')
            return redirect('profiles:chat_detail', chat_id)
        message.content = edited_message
        message.edited_at = timezone.now()
        message.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message_id': message.pk,
                'content': edited_message,
                'edited_at': message.edited_at,
            })
        messages.success(request, 'Message edited successfully')
        return redirect('profiles:chat_detail', chat_id)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        messages.error(request, f'{e}')
        return redirect('profiles:active_chats')
