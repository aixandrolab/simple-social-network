from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from friends.views.accept_friendship_request import accept_friendship_request_view
from friends.views.cancel_friendship_request import cancel_friendship_request_view
from friends.views.delete_friendship import delete_friendship_view
from friends.views.friends_list import friends_list_view
from friends.views.incoming_friendship_requests import incoming_friendship_requests_view
from friends.views.outgoing_friendship_reqeusts import outgoing_friendship_requests_view
from friends.views.reject_friendship_request import reject_friendship_request_view
from friends.views.send_friendship_request import send_friendship_request_view

app_name = 'friends'

urlpatterns = [
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
