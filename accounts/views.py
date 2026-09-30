from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import StudentProfile, UniversityFollow
from uni.models import University
from post.models import Post
from admissions.models import AdmissionUpdate

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")

        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # StudentProfile.objects.create(user=user)

        login(request, user)

        messages.success(
            request,
            "Welcome to the Scoolmasite & Admissions Platform!"
        )

        return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):

    logout(request)

    messages.success(request, "You have been logged out.")

    return redirect("home")

@login_required
def profile_view(request):

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    universities = University.objects.filter(
        is_verified=True
    ).order_by("name")

    if request.method == "POST":

        university_id = request.POST.get("university")
        role = request.POST.get("role", "").strip()
        location = request.POST.get("location", "").strip()
        bio = request.POST.get("bio", "").strip()

        # -------------------------------------------------
        # UNIVERSITY
        # -------------------------------------------------

        if university_id:

            profile.university = get_object_or_404(
                University,
                id=university_id
            )

        else:

            profile.university = None

        # -------------------------------------------------
        # ROLE
        # -------------------------------------------------

        valid_roles = {
            choice[0]
            for choice in StudentProfile.ROLE_CHOICES
        }

        if role in valid_roles:
            profile.role = role

        # -------------------------------------------------
        # OTHER PROFILE INFORMATION
        # -------------------------------------------------

        profile.location = location
        profile.bio = bio

        # -------------------------------------------------
        # PROFILE PICTURE
        # -------------------------------------------------

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES[
                "profile_picture"
            ]

        profile.save()

        messages.success(
            request,
            "Your profile has been updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "universities": universities,
            "role_choices": StudentProfile.ROLE_CHOICES,
        }
    )

    
@login_required
def follow_university(request, university_id):

    university = get_object_or_404(
        University,
        id=university_id
    )

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    UniversityFollow.objects.get_or_create(
        student=profile,
        university=university
    )

    messages.success(
        request,
        f"You are now following {university.name}."
    )

    return redirect(
        "university_detail",
        university_id=university.slug
    )


@login_required
def unfollow_university(request, university_id):

    university = get_object_or_404(
        University,
        id=university_id
    )

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    UniversityFollow.objects.filter(
        student=profile,
        university=university
    ).delete()

    messages.success(
        request,
        f"You have unfollowed {university.name}."
    )

    return redirect(
        "university_detail",
        university_id=university.slug
    )

@login_required
def dashboard_view(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    followed_universities = University.objects.filter(
        followers__student=profile
    ).distinct()

    recent_posts = Post.objects.filter(
        university__followers__student=profile,
        is_published=True
    ).select_related(
        "author",
        "university",
        "category"
    ).distinct()[:20]

    recent_admissions = AdmissionUpdate.objects.filter(
        university__followers__student=profile,
        is_published=True
    ).select_related(
        "university"
    ).distinct()[:20]
    

    return render(
        request,
        "accounts/dashboard.html",
        {
            "profile": profile,
            "followed_universities": followed_universities,
            "recent_posts": recent_posts,
            "recent_admissions": recent_admissions,
        }
    )