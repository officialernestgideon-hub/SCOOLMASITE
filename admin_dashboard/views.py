from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
        .filter(
            visit_count__gt=1
        )
        .count()
    )


    # -----------------------------
    # VISITOR CHART PERIOD
    # -----------------------------

    visitor_period = request.GET.get(
        "period",
        "7d"
    ).lower()

    if visitor_period not in ["7d", "30d", "3m"]:
        visitor_period = "7d"


    visitor_trend = []


    # -----------------------------
    # 7 DAYS
    # -----------------------------

    if visitor_period == "7d":

        start_date = today - timedelta(days=6)

        for i in range(7):

            day = start_date + timedelta(days=i)

            visits = SiteVisit.objects.filter(
                created_at__date=day
            )

            visitor_count = (
                visits
                .values("session_key")
                .distinct()
                .count()
            )

            visitor_trend.append({
                "date": day.strftime("%a"),
                "visitors": visitor_count,
                "page_views": visits.count(),
            })


    # -----------------------------
    # 30 DAYS
    # -----------------------------

    elif visitor_period == "30d":

        start_date = today - timedelta(days=29)

        for i in range(30):

            day = start_date + timedelta(days=i)

            visits = SiteVisit.objects.filter(
                created_at__date=day
            )

            visitor_count = (
                visits
                .values("session_key")
                .distinct()
                .count()
            )

            visitor_trend.append({
                "date": day.strftime("%d %b"),
                "visitors": visitor_count,
                "page_views": visits.count(),
            })


    # -----------------------------
    # 3 MONTHS
    # -----------------------------

    elif visitor_period == "3m":

        start_date = today - timedelta(days=89)

        current_date = start_date

        while current_date <= today:

            week_end = min(
                current_date + timedelta(days=6),
                today
            )

            visits = SiteVisit.objects.filter(
                created_at__date__gte=current_date,
                created_at__date__lte=week_end
            )

            visitor_count = (
                visits
                .values("session_key")
                .distinct()
                .count()
            )

            visitor_trend.append({
                "date": (
                    f"{current_date.strftime('%d %b')}"
                    f" - "
                    f"{week_end.strftime('%d %b')}"
                ),
                "visitors": visitor_count,
                "page_views": visits.count(),
            })

            current_date = week_end + timedelta(days=1)


    # -----------------------------
    # SCALE CHART BARS
    # -----------------------------

    max_visitors = max(
        (
            item["visitors"]
            for item in visitor_trend
        ),
        default=0
    )

    for item in visitor_trend:

        if max_visitors > 0:

            item["height"] = round(
                (
                    item["visitors"]
                    / max_visitors
                ) * 100
            )

        else:

            item["height"] = 0


    # Popular pages
    popular_pages = (
        SiteVisit.objects
        .values("path")
        .annotate(
            total=Count("id")
        )
        .order_by("-total")[:8]
    )

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
    
@login_required
def user_detail(request, user_id):

    if not request.user.is_staff:
        return render(
            request,
            "admin_dashboard/no_access.html",
            status=403
        )

    user = get_object_or_404(
        User.objects.select_related(
            "student_profile",
            "student_profile__university",
        ),
        id=user_id
    )

    if request.method == "POST":

        action = request.POST.get("action")

        # -----------------------------
        # EDIT USER
        # -----------------------------
        if action == "edit_user":

            first_name = request.POST.get(
                "first_name", ""
            ).strip()

            last_name = request.POST.get(
                "last_name", ""
            ).strip()

            email = request.POST.get(
                "email", ""
            ).strip()

            username = request.POST.get(
                "username", ""
            ).strip()

            location = request.POST.get(
                "location", ""
            ).strip()

            bio = request.POST.get(
                "bio", ""
            ).strip()

            if not username:
                messages.error(
                    request,
                    "Username cannot be empty."
                )

            elif User.objects.filter(
                username=username
            ).exclude(id=user.id).exists():

                messages.error(
                    request,
                    "That username is already in use."
                )

            elif email and User.objects.filter(
                email=email
            ).exclude(id=user.id).exists():

                messages.error(
                    request,
                    "That email address is already in use."
                )

            else:

                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                profile = user.student_profile
                profile.location = location
                profile.bio = bio
                profile.save()

                messages.success(
                    request,
                    f"{user.username}'s account has been updated."
                )

                return redirect(
                    "admin_user_detail",
                    user_id=user.id
                )


        # -----------------------------
        # VERIFY / UNVERIFY USER
        # -----------------------------
        elif action == "toggle_verification":

            profile = user.student_profile

            profile.is_verified = not profile.is_verified
            profile.save()

            if profile.is_verified:

                messages.success(
                    request,
                    f"{user.username} has been verified."
                )

            else:

                messages.success(
                    request,
                    f"Verification removed from {user.username}."
                )

            return redirect(
                "admin_user_detail",
                user_id=user.id
            )


        # -----------------------------
        # ACTIVATE / DEACTIVATE USER
        # -----------------------------
        elif action == "toggle_active":

            # Prevent an admin from disabling
            # their own account accidentally.
            if user.id == request.user.id:

                messages.error(
                    request,
                    "You cannot deactivate your own admin account."
                )

            else:

                user.is_active = not user.is_active
                user.save()

                if user.is_active:

                    messages.success(
                        request,
                        f"{user.username}'s account has been activated."
                    )

                else:

                    messages.success(
                        request,
                        f"{user.username}'s account has been deactivated."
                    )

            return redirect(
                "admin_user_detail",
                user_id=user.id
            )

    return render(
        request,
        "admin_dashboard/user_detail.html",
        {
            "user_account": user,
        }
    )