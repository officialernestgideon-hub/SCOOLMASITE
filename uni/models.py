from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)

    country = models.CharField(max_length=100, default="Nigeria")
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="universities/logos/",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="universities/covers/",
        blank=True,
        null=True
    )

    website = models.URLField(blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short_name or self.name
    
