from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles.views.auth_views.logout import logout_view
from profiles.views.chat_views.archive_chat import archive_chat_view
from profiles.views.chat_views.create_chat import create_chat_view
from profiles.views.chat_views.delete_chat import delete_chat_view
from profiles.views.chat_views.active_chats import active_chats_view
from profiles.views.chat_views.archived_chats import archived_chats_view
from profiles.views.chat_views.chat_detail import chat_detail_view
from profiles.views.chat_views.delete_message import delete_message_view
from profiles.views.chat_views.deleted_chats import deleted_chats_view
from profiles.views.chat_views.edit_message import edit_message_view
from profiles.views.chat_views.restore_chat import restore_chat_view
from profiles.views.chat_views.send_message import send_message_view
from profiles.views.chat_views.unarchive_chat import unarchive_chat_view
from profiles.views.friendship_views.accept_friendship_request import accept_friendship_request_view
from profiles.views.friendship_views.cancel_friendship_request import cancel_friendship_request_view
from profiles.views.friendship_views.delete_friendship import delete_friendship_view
from profiles.views.friendship_views.friends_list import friends_list_view
from profiles.views.friendship_views.incoming_friendship_requests import incoming_friendship_requests_view
from profiles.views.friendship_views.outgoing_friendship_reqeusts import outgoing_friendship_requests_view
from profiles.views.friendship_views.reject_friendship_request import reject_friendship_request_view
from profiles.views.friendship_views.send_friendship_request import send_friendship_request_view
from profiles.views.profile_views.profile_detail import profile_detail_view
from profiles.views.profile_views.profile_search import profile_search_view
from profiles.views.profile_views.upload_image import upload_image_view
from profiles.views.settings_views.change_password import change_password_view
from profiles.views.settings_views.settings import settings_view
from profiles.views.two_factor_views.two_factor_backup_codes import two_factor_backup_codes_view
from profiles.views.two_factor_views.two_factor_disable import two_factor_disable_view
from profiles.views.two_factor_views.two_factor_manage import two_factor_manage_view
from profiles.views.two_factor_views.two_factor_setup import two_factor_setup_view
from profiles.views.two_factor_views.two_factor_verify import two_factor_verify_view


app_name = 'profiles'

urlpatterns = [
    path('detail/<str:slug>/', profile_detail_view, name='profile_detail'),
    path('search/', profile_search_view, name='profile_search'),
    path('upload-image/', upload_image_view, name='upload_image'),

    path('logout/', logout_view, name='logout'),

    path('settings/', settings_view, name='settings'),
    path('change-password/', change_password_view, name='change_password'),

    path('two-factor/verify/', two_factor_verify_view, name='two_factor_verify'),
    path('two-factor/setup/', two_factor_setup_view, name='two_factor_setup'),
    path('two-factor/backup-codes/', two_factor_backup_codes_view, name='two_factor_backup_codes'),
    path('two-factor/manange/', two_factor_manage_view, name='two_factor_manage'),
    path('two-factor/disable/', two_factor_disable_view, name='two_factor_disable'),

    path('send/friend-request/<int:user_id>/', send_friendship_request_view, name='send_friendship_request'),
    path('accept/friedship-request/<int:friendship_id>/', accept_friendship_request_view,
         name='accept_friendship_request'),
    path('reject/friedship-request/<int:friendship_id>/', reject_friendship_request_view,
         name='reject_friendship_request'),
    path('cancel/friedship-requst/<int:friendship_id>/', cancel_friendship_request_view,
         name='cancel_friendship_request'),
    path('delete/friendship/<int:user_id>/', delete_friendship_view, name='delete_friendship'),
    path('incoming/friendship-requests/', incoming_friendship_requests_view,
         name='incoming_friendship_requests'),
    path('outgoing/friendship-requests/', outgoing_friendship_requests_view,
         name='outgoing_friendship_reqeusts'),
    path('@<str:username>/', friends_list_view, name='friends_list'),

    path('chats/active/', active_chats_view, name='active_chats'),
    path('chats/archived/', archived_chats_view, name='archived_chats'),
    path('chats/deleted/', deleted_chats_view, name='deleted_chats'),
    path('chat/create/<int:profile_id>/', create_chat_view, name='create_chat'),

    path('chat/delete/<int:chat_id>/', delete_chat_view, name='delete_chat'),
    path('chat/restore/<int:chat_id>/', restore_chat_view, name='restore_chat'),
    path('chat/archive/<int:chat_id>/', archive_chat_view, name='archive_chat'),
    path('chat/unarchive/<int:chat_id>/', unarchive_chat_view, name='unarchive_chat'),

    path('chat/details/<int:chat_id>/', chat_detail_view, name='chat_detail'),
    path('chat/<int:chat_id>/send/message/', send_message_view, name='send_message'),
    path('chat/<int:chat_id>/delete/message/<int:message_id>/', delete_message_view, name='delete_message'),
    path('chat/<int:chat_id>/edit/message/<int:message_id>/', edit_message_view, name='edit_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
