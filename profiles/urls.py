from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_detail_view, name='profile_detail'),
    path('logout/', views.logout_view, name='logout')
]