from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "universities/",
        views.university_list,
        name="university_list"
    ),

    path(
        "universities/<int:university_id>/",
        views.university_detail,
        name="university_detail"
    ),
]