from django.contrib import admin

from profiles.models.profile_model import Profile
from profiles.models.email_verification_token_model import EmailVerificationToken
from profiles.models.password_reset_token_model import PasswordResetToken
from profiles.models.friendship_models import Friendship, FriendshipHistory

admin.site.register(Profile)
admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)
admin.site.register(Friendship)
admin.site.register(FriendshipHistory)
