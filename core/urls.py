from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('confirm-register/<str:token>/', views.confirm_register_view, name='confirm_register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('resend-forgot-password/', views.resend_forgot_password_view, name='resend_forgot_password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password')
]
