from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AdmissionUpdate


@admin.register(AdmissionUpdate)
class AdmissionUpdateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "university",
        "admission_session",
        "is_verified",
        "is_published",
        "created_at",
    )

    list_filter = (
        "university",
        "is_verified",
        "is_published",
    )

    search_fields = (
        "title",
        "content",
        "university__name",
    )