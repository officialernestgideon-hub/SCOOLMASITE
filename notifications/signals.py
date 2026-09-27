from django.db.models.signals import post_save
from django.dispatch import receiver

from admissions.models import AdmissionUpdate
from accounts.models import UniversityFollow

from .models import Notification


@receiver(post_save, sender=AdmissionUpdate)
def create_admission_notifications(sender, instance, **kwargs):

    # Only notify when the update is both
    # published and verified.
    if not instance.is_published:
        return

    if not instance.is_verified:
        return

    # Find all students following this university
    follows = UniversityFollow.objects.filter(
        university=instance.university
    ).select_related(
        "student__user"
    )

    for follow in follows:

        Notification.objects.get_or_create(
            recipient=follow.student.user,
            admission_update=instance,

            defaults={
                "university": instance.university,

                "notification_type": "admission",

                "title": (
                    f"New admission update from "
                    f"{instance.university.short_name or instance.university.name}"
                ),

                "message": instance.title,
            }
        )