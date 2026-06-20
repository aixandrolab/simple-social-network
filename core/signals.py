# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import SiteConfig

@receiver(post_save, sender=SiteConfig)
def clear_site_config_cache(sender, instance, **kwargs):
    cache.delete('site_config_cache')
