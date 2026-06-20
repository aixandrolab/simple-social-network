# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals
