# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django.db import models

from profiles.models import Profile

STATUS_CHOICES = [
    ('PENDING', 'PENDING'),
    ('ACCEPTED', 'ACCEPTED'),
    ('REJECTED', 'REJECTED'),
]

class FriendshipStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'

class Friendship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_friendships')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_friendships')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name="unique_friendship"
            )
        ]
        indexes = [
            models.Index(fields=['sender', 'receiver', 'status']),
            models.Index(fields=['receiver', 'sender', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
        ]

    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.status})'

    def accept(self):
        self.status = FriendshipStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = FriendshipStatus.REJECTED
        self.save()


class FriendshipHistory(models.Model):
    friendship = models.ForeignKey(
        Friendship,
        on_delete=models.CASCADE,
        related_name='friendship_history',
    )
    old_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    new_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'friendship history'
        verbose_name = 'friendship history'

        indexes = [
            models.Index(fields=['friendship']),
            models.Index(fields=['changed_at']),
            models.Index(fields=['new_status']),
        ]

    def __str__(self):
        return f'{self.friendship}: {self.old_status} -> {self.new_status}'
