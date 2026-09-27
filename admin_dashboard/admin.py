from django.contrib import admin
from .models import SiteVisit


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):

    list_display = (
        "path",
        "user",
        "device_type",
        "browser",
        "operating_system",
        "country",
        "created_at",
    )

    list_filter = (
        "device_type",
        "browser",
        "operating_system",
        "country",
        "created_at",
    )

    search_fields = (
        "path",
        "country",
        "browser",
        "operating_system",
        "ip_address",
    )

    ordering = ("-created_at",)