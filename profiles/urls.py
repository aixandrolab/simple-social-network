from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles.views.auth_views.logout_view import logout_view
from profiles.views.profile_views.profile_detail_view import profile_detail_view
from profiles.views.profile_views.profile_search_view import profile_search_view
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

    path('logout/', logout_view, name='logout'),

    path('settings/', settings_view, name='settings'),
    path('change-password/', change_password_view, name='change_password'),

    path('two-factor/verify/', two_factor_verify_view, name='two_factor_verify'),
    path('two-factor/setup/', two_factor_setup_view, name='two_factor_setup'),
    path('two-factor/backup-codes/', two_factor_backup_codes_view, name='two_factor_backup_codes'),
    path('two-factor/manange/', two_factor_manage_view, name='two_factor_manage'),
    path('two-factor/disable/', two_factor_disable_view, name='two_factor_disable'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
