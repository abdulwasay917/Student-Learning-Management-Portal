from django.db import models
from django.utils import timezone
from datetime import timedelta

from accounts.models import User


class Meeting(models.Model):

    title = models.CharField(max_length=255)

    link = models.URLField()

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="meetings"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):

        if not self.pk:
            self.expires_at = (
                timezone.now()
                + timedelta(hours=12)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title