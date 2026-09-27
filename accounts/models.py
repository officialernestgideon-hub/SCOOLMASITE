from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class StudentProfile(models.Model):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("applicant", "Admission Applicant"),
        ("alumni", "Alumni"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    university = models.ForeignKey(
        "uni.University",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    location = models.CharField(
        max_length=150,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    
class UniversityFollow(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="university_follows"
    )

    university = models.ForeignKey(
        "uni.University",
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "university"],
                name="unique_university_follow"
            )
        ]

    def __str__(self):
        return f"{self.student} follows {self.university}"
    
    @receiver(post_save, sender=User)
    def create_student_profile(sender, instance, created, **kwargs):

        if created:

            StudentProfile.objects.get_or_create(
                user=instance
            )
