from django.db.models import Q
from django.shortcuts import render

from uni.models import University
from admissions.models import AdmissionUpdate
from post.models import Post


def search(request):

    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    state = request.GET.get("state", "").strip()
    session = request.GET.get("session", "").strip()

    # -------------------------
    # FILTER OPTIONS
    # -------------------------

    countries = (
        University.objects
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )

    states = (
        University.objects
        .values_list("state", flat=True)
        .exclude(state="")
        .distinct()
        .order_by("state")
    )

    sessions = (
        AdmissionUpdate.objects
        .values_list("admission_session", flat=True)
        .exclude(admission_session="")
        .distinct()
        .order_by("-admission_session")
    )

    # Empty querysets by default
    universities = University.objects.none()
    admissions = AdmissionUpdate.objects.none()
    student_posts = Post.objects.none()

    # Only perform searches when something was entered/selected
    if query or country or state or session:

        # -------------------------
        # UNIVERSITIES
        # -------------------------

        universities = University.objects.all()

        if query:
            universities = universities.filter(
                Q(name__icontains=query) |
                Q(short_name__icontains=query) |
                Q(state__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )

        if country:
            universities = universities.filter(
                country__iexact=country
            )

        if state:
            universities = universities.filter(
                state__iexact=state
            )

        universities = universities.order_by("name")


        # -------------------------
        # ADMISSION UPDATES
        # -------------------------

        admissions = AdmissionUpdate.objects.filter(
            is_published=True
        )

        if query:
            admissions = admissions.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(admission_session__icontains=query) |
                Q(university__name__icontains=query) |
                Q(university__short_name__icontains=query)
            )

        if country:
            admissions = admissions.filter(
                university__country__iexact=country
            )

        if state:
            admissions = admissions.filter(
                university__state__iexact=state
            )

        if session:
            admissions = admissions.filter(
                admission_session__iexact=session
            )

        admissions = (
            admissions
            .select_related("university")
            .order_by("-created_at")
        )


        # -------------------------
        # STUDENT POSTS
        # -------------------------

        student_posts = Post.objects.filter(
            is_published=True
        )

        if query:
            student_posts = student_posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(university__name__icontains=query) |
                Q(university__short_name__icontains=query) |
                Q(university__state__icontains=query) |
                Q(university__country__icontains=query) |
                Q(category__name__icontains=query)
            )

        if country:
            student_posts = student_posts.filter(
                university__country__iexact=country
            )

        if state:
            student_posts = student_posts.filter(
                university__state__iexact=state
            )

        student_posts = (
            student_posts
            .select_related(
                "author",
                "university",
                "category"
            )
            .order_by("-created_at")
        )

    return render(
        request,
        "discovery/search.html",
        {
            "query": query,
            "country": country,
            "state": state,
            "session": session,

            "countries": countries,
            "states": states,
            "sessions": sessions,

            "universities": universities,
            "admissions": admissions,
            "student_posts": student_posts,
        }
    )