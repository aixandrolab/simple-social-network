# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import admin

from profiles.models.profile_model import Profile
from profiles.models.email_verification_token_model import EmailVerificationToken
from profiles.models.password_reset_token_model import PasswordResetToken

admin.site.register(Profile)
admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)
