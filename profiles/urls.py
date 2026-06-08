from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles.views.auth_views.logout_view import logout_view
from profiles.views.chat_views.active_chats_view import active_chats_view
from profiles.views.friendship_views.accept_friendship_request_view import accept_friendship_request_view
from profiles.views.friendship_views.cancel_friendship_request_view import cancel_friendship_request_view
from profiles.views.friendship_views.delete_friendship_view import delete_friendship_view
from profiles.views.friendship_views.friends_list_view import friends_list_view
from profiles.views.friendship_views.incoming_friendship_requests_view import incoming_friendship_requests_view
from profiles.views.friendship_views.outgoing_friendship_reqeusts_view import outgoing_friendship_requests_view
from profiles.views.friendship_views.reject_friendship_request_view import reject_friendship_request_view
from profiles.views.friendship_views.send_friendship_request_view import send_friendship_request_view
from profiles.views.profile_views.profile_detail_view import profile_detail_view
from profiles.views.profile_views.profile_search_view import profile_search_view
from profiles.views.profile_views.upload_image_view import upload_image_view
from profiles.views.settings_views.change_password_view import change_password_view
from profiles.views.settings_views.settings_view import settings_view
from profiles.views.two_factor_views.two_factor_backup_codes_view import two_factor_backup_codes_view
from profiles.views.two_factor_views.two_factor_disable_view import two_factor_disable_view
from profiles.views.two_factor_views.two_factor_manage_view import two_factor_manage_view
from profiles.views.two_factor_views.two_factor_setup_view import two_factor_setup_view
from profiles.views.two_factor_views.two_factor_verify_view import two_factor_verify_view


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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
