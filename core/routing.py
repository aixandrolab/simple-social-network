from django.urls import re_path

from core.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
]