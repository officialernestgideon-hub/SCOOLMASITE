from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short_name or self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2

            while University.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    
