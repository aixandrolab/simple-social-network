from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from chats.views.active_chats import active_chats_view
from chats.views.archive_chat import archive_chat_view
from chats.views.archived_chats import archived_chats_view
from chats.views.chat_detail import chat_detail_view
from chats.views.chat_settings import chat_settings_view
from chats.views.clear_chat import clear_chat_view
from chats.views.create_chat import create_chat_view
from chats.views.delete_chat import delete_chat_view
from chats.views.deleted_chats import deleted_chats_view
from chats.views.mute_chat import mute_chat_view
from chats.views.restore_chat import restore_chat_view

app_name = 'chats'

urlpatterns = [
    path('chats/active/', active_chats_view, name='active_chats'),
    path('chats/archived/', archived_chats_view, name='archived_chats'),
    path('chats/deleted/', deleted_chats_view, name='deleted_chats'),

    path('chat/create/<int:profile_id>/', create_chat_view, name='create_chat'),
    path('chat/settings/<int:chat_id>/', chat_settings_view, name='chat_settings'),

    path('chat/delete/<int:chat_id>/', delete_chat_view, name='delete_chat'),
    path('chat/restore/<int:chat_id>/', restore_chat_view, name='restore_chat'),
    path('chat/archive/<int:chat_id>/', archive_chat_view, name='archive_chat'),
    path('chat/mute/<int:chat_id>/', mute_chat_view, name='mute_chat'),

    path('chat/details/<int:chat_id>/', chat_detail_view, name='chat_detail'),
    path('chat/<int:chat_id>/clear/', clear_chat_view, name='clear_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
