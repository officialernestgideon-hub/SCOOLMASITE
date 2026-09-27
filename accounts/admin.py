from django.contrib import admin

# Register your models here.

from .models import StudentProfile, UniversityFollow


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "university",
        "role",
        "is_verified",
    )

    list_filter = (
        "role",
        "is_verified",
    )

    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(UniversityFollow)
class UniversityFollowAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "university",
        "created_at",
    )

    search_fields = (
        "student__user__username",
        "university__name",
    )
