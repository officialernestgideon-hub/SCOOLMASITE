from django.db import models


class SiteVisit(models.Model):

    session_key = models.CharField(
        max_length=100,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="site_visits"
    )

    path = models.CharField(
        max_length=500,
        db_index=True
    )

    referrer = models.URLField(
        blank=True
    )
    
    traffic_source = models.CharField(
        max_length=50,
        blank=True,
        db_index=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    device_type = models.CharField(
        max_length=30,
        blank=True
    )

    browser = models.CharField(
        max_length=100,
        blank=True
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.path} - {self.created_at}"
