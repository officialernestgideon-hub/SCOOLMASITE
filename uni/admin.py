from django.contrib import admin

# Register your models here.

from .models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "country",
        "state",
        "is_verified",
    )

    list_filter = (
        "country",
        "is_verified",
    )

    search_fields = (
        "name",
        "short_name",
        "state",
        "city",
    )
    
    readonly_fields = ("slug",)
