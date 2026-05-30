from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles.views.auth_views.logout_view import logout_view
from profiles.views.profile_views.profile_detail_view import profile_detail_view
from profiles.views.settings_views.change_password_view import change_password_view
from profiles.views.settings_views.settings_view import settings_view


app_name = 'profiles'

urlpatterns = [
    path('', profile_detail_view, name='profile_detail'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
    path('change-password/', change_password_view, name='change_password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
