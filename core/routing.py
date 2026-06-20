# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.urls import re_path

from core import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
