from django.contrib import admin

from profiles.models.profile_model import Profile
from profiles.models.email_verification_token_model import EmailVerificationToken

admin.site.register(Profile)
admin.site.register(EmailVerificationToken)
