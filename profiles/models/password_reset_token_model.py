import secrets
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name="password_reset_token"
    )
    token = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def use_token(self):
        self.token = True
        self.delete()

    @classmethod
    def create_token(cls, user):
        cls.objects.filter(user=user, is_used=False).delete()

        token = secrets.token_urlsafe(32)
        return cls.objects.create(user=user, token=token)

    @classmethod
    def cleanup_expired_tokens(cls):
        expiration_time = timezone.now() - timedelta(hours=24)
        deleted_count = cls.objects.filter(
            created_at__lte=expiration_time,
            is_used=False
        ).delete()
        return deleted_count[0]
