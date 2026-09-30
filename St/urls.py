"""
URL configuration for St project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts import views

urlpatterns = [
    # TEMPORARY - remove after creating production admin
    path("setup-production-admin/", views.setup_production_admin, name="setup_production_admin"),
    
    # Custom admin dashboard
    path("admin/", include("admin_dashboard.urls")),

    # Django built-in admin
    path("django-admin/", admin.site.urls),
    
    path(
        "accounts/",
        include("accounts.urls")
    ),

    path(
        "",
        include("uni.urls")
    ),
    
    path(
        "posts/",
        include("post.urls")
    ),
    
    path(
        "notifications/",
        include("notifications.urls")
    ),
    
    path(
        "admissions/",
        include("admissions.urls")
    ),
    
    path(
        "search/",
        include("discovery.urls")
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
