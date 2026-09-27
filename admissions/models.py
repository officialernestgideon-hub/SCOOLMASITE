from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AdmissionUpdate(models.Model):

    university = models.ForeignKey(
        "uni.University",
        on_delete=models.CASCADE,
        related_name="admission_updates"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admission_updates"
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    admission_session = models.CharField(
        max_length=50,
        blank=True
    )

    application_start = models.DateField(
        null=True,
        blank=True
    )

    application_deadline = models.DateField(
        null=True,
        blank=True
    )

    official_link = models.URLField(
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.university} - {self.title}"
