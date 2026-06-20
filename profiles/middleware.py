# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from profiles.models.profile_model import Profile


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        user = request.user
        now = timezone.now()
        cache_key = f"user_{user.id}_last_activity"

        cache.set(cache_key, now, timeout=300)

        if user.profile.last_activity is None or (now - user.profile.last_activity) >= timedelta(minutes=5):
            Profile.objects.filter(user=user).update(last_activity=now)
            user.profile.last_activity = now
