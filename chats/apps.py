# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'chats'

    def ready(self):
        import chats.signals
