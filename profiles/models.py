import secrets
import uuid
from datetime import timedelta

import bcrypt
import pyotp
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache


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
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        editable=True,
        verbose_name='URL slug'
    )
    email = models.EmailField(unique=True)
    biography = models.TextField(default="Hi, I'm new here!")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDERS, default='O', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    two_fa_secret = models.CharField(max_length=255, null=True, blank=True)
    is_2fa_active = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)
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

    def enable_2fa(self, secret):
        self.two_fa_secret = secret
        self.is_2fa_active = True
        self.save()

    def disable_2fa(self):
        self.two_fa_secret = None
        self.is_2fa_active = False
        self.backup_codes = []
        self.save()

    def generate_backup_codes(self, num_codes=10):
        codes = []
        plain_codes = []

        for _ in range(num_codes):
            code = secrets.token_urlsafe(8).upper()[:8]
            hashed = bcrypt.hashpw(code.encode(), bcrypt.gensalt()).decode()
            codes.append(hashed)
            plain_codes.append(code)

        self.backup_codes = codes
        self.save()
        return plain_codes

    def verify_backup_code(self, code):
        for i, hashed_code in enumerate(self.backup_codes):
            if bcrypt.checkpw(code.encode(), hashed_code.encode()):
                backup_list = list(self.backup_codes)
                backup_list.pop(i)
                self.backup_codes = backup_list
                self.save()
                return True
        return False

    def get_totp_device(self):
        if self.two_fa_secret:
            return pyotp.TOTP(self.two_fa_secret, interval=30)
        return None

    @property
    def is_online(self):
        last_active = cache.get(f'user_{self.user.id}_last_activity')

        if last_active is None:
            last_active = self.last_activity

        if last_active is None:
            return False

        return timezone.now() - last_active < timedelta(minutes=5)

    def verify_totp(self, code):
        totp = self.get_totp_device()
        if totp:
            return totp.verify(code, valid_window=1)
        return False

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default_avatar.png'

    def get_absolute_url(self):
        return reverse('profiles:profile_detail', args=[self.slug])

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
