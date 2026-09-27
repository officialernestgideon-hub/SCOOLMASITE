from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ("admission", "Admission Update"),
        ("post", "University Post"),
        ("system", "System Notification"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    university = models.ForeignKey(
        "uni.University",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    admission_update = models.ForeignKey(
        "admissions.AdmissionUpdate",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default="system"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "recipient",
                    "admission_update"
                ],
                name="unique_admission_notification"
            )
        ]

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"