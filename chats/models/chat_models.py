from django.db import models
from django.utils import timezone

from profiles.models import Profile


class Chat(models.Model):
    user1 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="user1_participant",
        db_index=True
    )
    user2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="user2_participant",
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(f"{self.name}")


class ChatStatus(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat_statuses",
        db_index=True
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_statuses",
        db_index=True
    )
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    muted_at = models.DateTimeField(null=True, blank=True)
    cleared_at = models.DateTimeField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)

    is_initiator = models.BooleanField(default=False)

    class Meta:
        unique_together = ["chat", "profile"]
        indexes = [
            models.Index(fields=["profile", "is_archived"]),
        ]
        verbose_name_plural = "chat statuses"
        verbose_name = "chat status"

    def save(self, *args, **kwargs):
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        if self.is_archived and not self.archived_at:
            self.archived_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Status of #{self.chat.id} - {self.profile.user.username}"
