from django.urls import path

from . import views


urlpatterns = [
    path(
        "<int:admission_id>/",
        views.admission_detail,
        name="admission_detail"
    ),
]