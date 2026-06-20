# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import admin

from chats.models import Chat, ChatStatus, ChatMessage, ChatMessageStatus

admin.register(Chat)
admin.register(ChatStatus)
admin.register(ChatMessage)
admin.register(ChatMessageStatus)
