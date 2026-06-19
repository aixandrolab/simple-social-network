from django.apps import AppConfig


class ChatsConfig(AppConfig):
    name = 'chats'

    def ready(self):
        import chats.signals
