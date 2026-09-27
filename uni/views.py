from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import University
from accounts.models import StudentProfile, UniversityFollow
from django.shortcuts import get_object_or_404, render
from .models import University
from post.models import Post
# Create your views here.


def home(request):

    universities = University.objects.all().order_by(
        "-is_verified",
        "name"
    )[:6]

    trending_posts = Post.objects.filter(
        is_published=True
    ).select_related(
        "author",
        "university",
        "category"
    ).order_by(
        "-views_count",
        "-created_at"
    )[:4]

    latest_posts = Post.objects.filter(
        is_published=True
    ).select_related(
        "author",
        "university",
        "category"
    ).order_by(
        "-created_at"
    )[:6]

    return render(
        request,
        "home.html",
        {
            "universities": universities,
            "trending_posts": trending_posts,
            "latest_posts": latest_posts,
        }
    )


def university_list(request):

    universities = University.objects.all()

    query = request.GET.get("q", "").strip()

    if query:
        universities = universities.filter(
            name__icontains=query
        )

    return render(
        request,
        "universities/list.html",
        {
            "universities": universities,
            "query": query,
        }
    )


def university_detail(request, university_id):

    university = get_object_or_404(
        University,
        id=university_id
    )

    posts = university.posts.filter(
        is_published=True
    ).select_related(
        "author",
        "category"
    )[:20]

    admissions = university.admission_updates.filter(
        is_published=True
    )[:10]

    is_following = False

    if request.user.is_authenticated:

        try:
            profile = request.user.student_profile

            is_following = UniversityFollow.objects.filter(
                student=profile,
                university=university
            ).exists()

        except StudentProfile.DoesNotExist:

            is_following = False

    follower_count = UniversityFollow.objects.filter(
        university=university
    ).count()

    return render(
        request,
        "universities/detail.html",
        {
            "university": university,
            "posts": posts,
            "admissions": admissions,
            "is_following": is_following,
            "follower_count": follower_count,
        }
    )
    
    
