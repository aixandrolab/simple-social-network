from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from profiles.models.friendship_models import Friendship, FriendshipHistory
from profiles.models.profile_model import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email, slug=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=User)
def update_new_superuser(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            profile = Profile.objects.get(user=instance)
            profile.is_email_verified = True
            profile.save()

@receiver(pre_save, sender=Friendship)
def save_friendship_status(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_status = Friendship.objects.get(pk=instance.pk).status
        instance._old_status = old_status
    except Friendship.DoesNotExist:
        pass

@receiver(post_save, sender=Friendship)
def log_friendship_status_change(sender, instance, created, **kwargs):
    if created:
        return
    if hasattr(instance, '_old_status') and instance._old_status != instance.status:
        FriendshipHistory.objects.create(
            friendship=instance,
            old_status=instance._old_status,
            new_status=instance.status
        )
