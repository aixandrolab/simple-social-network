# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.urls import path

from core.views.auth_views.confirm_register import confirm_register_view
from core.views.auth_views.login import login_view
from core.views.auth_views.register import register_view
from core.views.home import home_view
from core.views.password_views.forgot_password import forgot_password_view
from core.views.password_views.resend_forgot_password import resend_forgot_password_view
from core.views.password_views.reset_password import reset_password_view

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('confirm-register/<str:token>/', confirm_register_view, name='confirm_register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('resend-forgot-password/', resend_forgot_password_view, name='resend_forgot_password'),
    path('reset-password/<str:token>/', reset_password_view, name='reset_password')
]
