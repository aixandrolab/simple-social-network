# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.apps import AppConfig


class FriendsConfig(AppConfig):
    name = 'friends'

    def ready(self):
        import friends.signals
