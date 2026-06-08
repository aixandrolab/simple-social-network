from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q, Model
from django.utils import timezone

from profiles.models import Chat, Profile


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True
    )
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_sent_messages",
        db_index=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender}: {self.content}"


class ChatMessageStatus(models.Model):
    message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name="statuses",
        db_index=True
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="message_statuses",
        db_index=True
    )
    is_cleared = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["message", "profile"]
        verbose_name_plural = "chat message statuses"
        verbose_name = "chat message status"
