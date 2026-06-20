# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals
