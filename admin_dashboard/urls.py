from django.urls import path
from . import views
from django.contrib.auth.models import User


urlpatterns = [
    path("", views.dashboard, name="admin_dashboard"),
    path("analytics/", views.analytics, name="admin_analytics"),
    path(
        "users/",
        views.users,
        name="admin_users"
    ),
]