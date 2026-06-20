# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.contrib import admin

from friends.models import Friendship, FriendshipHistory

admin.site.register(Friendship)
admin.site.register(FriendshipHistory)
