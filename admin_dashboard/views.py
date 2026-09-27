from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from accounts.models import StudentProfile
from admissions.models import AdmissionUpdate
from post.models import Post, Category
from uni.models import University

from .models import SiteVisit


@login_required
def dashboard(request):

    if not request.user.is_staff:
        return render(
            request,
            "admin_dashboard/no_access.html",
            status=403
        )

    now = timezone.now()
    today = now.date()

    # -----------------------------
    # VISITOR ANALYTICS
    # -----------------------------

    visitors_today = SiteVisit.objects.filter(
        created_at__date=today
    )

    page_views_today = visitors_today.count()

    unique_visitors_today = (
        visitors_today
        .values("session_key")
        .distinct()
        .count()
    )

    returning_visitors_today = (
        visitors_today
        .values("session_key")
        .annotate(
            visit_count=Count("id")
        )
        .filter(visit_count__gt=1)
        .count()
    )

    # Last 7 days
    seven_days_ago = now - timedelta(days=6)

    visitor_trend = []

    for i in range(7):
        day = (seven_days_ago + timedelta(days=i)).date()

        visits = SiteVisit.objects.filter(
            created_at__date=day
        )

        visitor_trend.append({
            "date": day.strftime("%a"),
            "visitors": visits.values(
                "session_key"
            ).distinct().count(),
            "page_views": visits.count(),
        })

    # Popular pages
    popular_pages = (
        SiteVisit.objects
        .values("path")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )

    # Devices
    devices = (
        SiteVisit.objects
        .exclude(device_type="")
        .values("device_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Browsers
    browsers = (
        SiteVisit.objects
        .exclude(browser="")
        .values("browser")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # -----------------------------
    # PLATFORM STATISTICS
    # -----------------------------

    context = {

        # Main statistics
        "total_users": User.objects.count(),
        "total_students": StudentProfile.objects.count(),
        "total_universities": University.objects.count(),
        "total_admissions": AdmissionUpdate.objects.count(),
        "total_posts": Post.objects.count(),
        "total_categories": Category.objects.count(),

        # Verification
        "verified_students": StudentProfile.objects.filter(
            is_verified=True
        ).count(),

        "verified_universities": University.objects.filter(
            is_verified=True
        ).count(),

        "verified_admissions": AdmissionUpdate.objects.filter(
            is_verified=True
        ).count(),

        "verified_posts": Post.objects.filter(
            is_verified=True
        ).count(),

        # Visitors
        "visitors_today": unique_visitors_today,
        "page_views_today": page_views_today,
        "returning_visitors_today": returning_visitors_today,

        # Charts / analytics
        "visitor_trend": visitor_trend,
        "popular_pages": popular_pages,
        "devices": devices,
        "browsers": browsers,

        # Recent activity
        "recent_users": User.objects.order_by(
            "-date_joined"
        )[:5],

        "recent_universities": University.objects.order_by(
            "-created_at"
        )[:5],

        "recent_admissions": AdmissionUpdate.objects.select_related(
            "university"
        ).order_by("-created_at")[:5],

        "recent_posts": Post.objects.select_related(
            "author",
            "university"
        ).order_by("-created_at")[:5],
    }

    return render(
        request,
        "admin_dashboard/dashboard.html",
        context
    )
    
@login_required
def analytics(request):

    if not request.user.is_staff:
        return render(
            request,
            "admin_dashboard/no_access.html",
            status=403
        )

    now = timezone.now()

    # -----------------------------
    # DATE RANGES
    # -----------------------------

    today = now.date()
    seven_days_ago = today - timedelta(days=6)
    thirty_days_ago = today - timedelta(days=29)

    # -----------------------------
    # VISITOR DATA
    # -----------------------------

    total_page_views = SiteVisit.objects.count()

    unique_visitors = (
        SiteVisit.objects
        .exclude(session_key="")
        .values("session_key")
        .distinct()
        .count()
    )

    returning_visitors = (
        SiteVisit.objects
        .exclude(session_key="")
        .values("session_key")
        .annotate(
            visits=Count("id")
        )
        .filter(visits__gt=1)
        .count()
    )

    visitors_today = (
        SiteVisit.objects
        .filter(created_at__date=today)
        .exclude(session_key="")
        .values("session_key")
        .distinct()
        .count()
    )

    page_views_today = SiteVisit.objects.filter(
        created_at__date=today
    ).count()

    visitors_week = (
        SiteVisit.objects
        .filter(created_at__date__gte=seven_days_ago)
        .exclude(session_key="")
        .values("session_key")
        .distinct()
        .count()
    )

    visitors_month = (
        SiteVisit.objects
        .filter(created_at__date__gte=thirty_days_ago)
        .exclude(session_key="")
        .values("session_key")
        .distinct()
        .count()
    )

    # -----------------------------
    # VISITOR TREND - LAST 7 DAYS
    # -----------------------------

    visitor_trend = []

    for i in range(7):

        day = seven_days_ago + timedelta(days=i)

        daily_visits = SiteVisit.objects.filter(
            created_at__date=day
        )

        unique_visitors = (
            daily_visits
            .exclude(session_key="")
            .values("session_key")
            .distinct()
            .count()
        )

        page_views = daily_visits.count()

        returning_visitors = (
            daily_visits
            .exclude(session_key="")
            .values("session_key")
            .annotate(
                visit_count=Count("id")
            )
            .filter(visit_count__gt=1)
            .count()
        )

        visitor_trend.append({
            "label": day.strftime("%a"),
            "date": day.strftime("%b %d"),
            "visitors": unique_visitors,
        "page_views": page_views,
        "returning": returning_visitors,
        })

    # -----------------------------
    # POPULAR PAGES
    # -----------------------------

    popular_pages = (
        SiteVisit.objects
        .values("path")
        .annotate(
            views=Count("id")
        )
        .order_by("-views")[:10]
    )

    # -----------------------------
    # DEVICES
    # -----------------------------

    devices = (
        SiteVisit.objects
        .exclude(device_type="")
        .values("device_type")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    # -----------------------------
    # BROWSERS
    # -----------------------------

    browsers = (
        SiteVisit.objects
        .exclude(browser="")
        .values("browser")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    # -----------------------------
    # OPERATING SYSTEMS
    # -----------------------------

    operating_systems = (
        SiteVisit.objects
        .exclude(operating_system="")
        .values("operating_system")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    # -----------------------------
    # REFERRERS
    # -----------------------------

    traffic_sources = (
        SiteVisit.objects
        .exclude(traffic_source="")
        .values("traffic_source")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # -----------------------------
    # COUNTRIES
    # -----------------------------

    countries = (
        SiteVisit.objects
        .exclude(country="")
        .values("country")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")[:10]
    )

    # -----------------------------
    # USER GROWTH
    # -----------------------------

    user_growth = []

    for i in range(7):

        day = seven_days_ago + timedelta(days=i)

        users = User.objects.filter(
            date_joined__date__lte=day
        ).count()

        user_growth.append({
            "label": day.strftime("%a"),
            "users": users,
        })

    # -----------------------------
    # CONTENT ANALYTICS
    # -----------------------------

    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(
        is_published=True
    ).count()

    total_universities = University.objects.count()
    verified_universities = University.objects.filter(
        is_verified=True
    ).count()

    total_admissions = AdmissionUpdate.objects.count()
    published_admissions = AdmissionUpdate.objects.filter(
        is_published=True
    ).count()

    # Most viewed posts
    popular_posts = (
        Post.objects
        .order_by("-views_count")[:10]
    )

    context = {

        # Visitors
        "total_page_views": total_page_views,
        "unique_visitors": unique_visitors,
        "returning_visitors": returning_visitors,
        "visitors_today": visitors_today,
        "page_views_today": page_views_today,
        "visitors_week": visitors_week,
        "visitors_month": visitors_month,

        # Trends
        "visitor_trend": visitor_trend,
        "user_growth": user_growth,

        # Traffic
        "popular_pages": popular_pages,
        "devices": devices,
        "browsers": browsers,
        "operating_systems": operating_systems,
        "traffic_sources": traffic_sources,
        "countries": countries,

        # Content
        "total_posts": total_posts,
        "published_posts": published_posts,
        "total_universities": total_universities,
        "verified_universities": verified_universities,
        "total_admissions": total_admissions,
        "published_admissions": published_admissions,
        "popular_posts": popular_posts,
    }

    return render(
        request,
        "admin_dashboard/analytics.html",
        context
    )

@login_required
def users(request):

    if not request.user.is_staff:
        return render(
            request,
            "admin_dashboard/no_access.html",
            status=403
        )

    users = (
        User.objects
        .select_related("student_profile")
        .order_by("-date_joined")
    )

    context = {
        "users": users,
    }

    return render(
        request,
        "admin_dashboard/users.html",
        context
    )