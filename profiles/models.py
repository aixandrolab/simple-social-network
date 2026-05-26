from django.contrib.auth.models import User
from django.db import models

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
    gender = models.CharField(choices=GENDERS, default='Not Specified', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'
        ordering = ['-pk']

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.username
