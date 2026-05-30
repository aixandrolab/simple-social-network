import uuid

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    biography = models.TextField(default="Hi, I'm new here!")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDERS, default='O', blank=True, null=True)
    is_active = models.BooleanField(default=True)
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
