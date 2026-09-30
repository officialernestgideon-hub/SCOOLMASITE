from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    
    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    path(
        "universities/",
        views.university_list,
        name="university_list"
    ),

    path(
        "universities/<slug:slug>/",
        views.university_detail,
        name="university_detail"
    ),
]