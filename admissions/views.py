from django.shortcuts import get_object_or_404, render

from .models import AdmissionUpdate


def admission_detail(request, admission_id):

    admission = get_object_or_404(
        AdmissionUpdate.objects.select_related("university", "author"),
        id=admission_id,
        is_published=True
    )

    return render(
        request,
        "admissions/detail.html",
        {
            "admission": admission,
        }
    )
