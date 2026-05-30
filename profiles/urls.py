from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_detail_view, name='profile_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('change-password/', views.change_password_view, name='change_password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
