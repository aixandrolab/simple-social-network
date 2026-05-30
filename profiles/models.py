import secrets
import uuid
from datetime import timedelta
from os import MFD_ALLOW_SEALING

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return f"user_avatars/user_{instance.user.id}/{new_filename}"

class Profile(models.Model):
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Not Specified')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(unique=True)
    biography = models.TextField(default="Hi, I'm new here!")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDERS, default='O', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'gif', 'webp'])
        ],
        verbose_name='Avatar'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        ordering = ['-pk']

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default_avatar.png'

    def get_absolute_url(self):
        return reverse('profiles:profile_detail')

    def __str__(self):
        return self.user.username


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='email_verification_token'
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
