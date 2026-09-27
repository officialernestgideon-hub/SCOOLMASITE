from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Category, Comment, Like, Post, PostView
from uni.models import University


@login_required
def create_post(request):

    universities = University.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":

        university_id = request.POST.get("university")
        category_id = request.POST.get("category")
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")

        if not university_id or not title or not content:
            messages.error(
                request,
                "Please select a university and fill in the title and content."
            )

            return render(
                request,
                "posts/create.html",
                {
                    "universities": universities,
                    "categories": categories,
                }
            )

        university = get_object_or_404(
            University,
            id=university_id
        )

        category = None

        if category_id:
            category = get_object_or_404(
                Category,
                id=category_id
            )

        Post.objects.create(
            author=request.user,
            university=university,
            category=category,
            title=title,
            content=content,
            image=image,
        )

        messages.success(
            request,
            "Your post has been published successfully."
        )

        return redirect(
            "university_detail",
            university_id=university.id
        )

    return render(
        request,
        "posts/create.html",
        {
            "universities": universities,
            "categories": categories,
        }
    )
    
def post_detail(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True
    )

    # Make sure anonymous visitors have a session
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Only count another view after 30 minutes
    thirty_minutes_ago = timezone.now() - timedelta(
        minutes=30
    )

    if request.user.is_authenticated:

        recent_view = PostView.objects.filter(
            post=post,
            user=request.user,
            created_at__gte=thirty_minutes_ago
        ).exists()

    else:

        recent_view = PostView.objects.filter(
            post=post,
            session_key=session_key,
            user__isnull=True,
            created_at__gte=thirty_minutes_ago
        ).exists()

    if not recent_view:

        PostView.objects.create(
            post=post,
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key
        )

        post.views_count += 1

        post.save(
            update_fields=["views_count"]
        )

    comments = post.comments.select_related(
        "user"
    ).all()

    liked = False

    if request.user.is_authenticated:

        liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()

    return render(
        request,
        "posts/detail.html",
        {
            "post": post,
            "comments": comments,
            "liked": liked,
        }
    )


@login_required
def like_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect(
        "post_detail",
        post_id=post.id
    )


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True
    )

    if request.method == "POST":

        content = request.POST.get(
            "content",
            ""
        ).strip()

        if not content:

            messages.error(
                request,
                "Comment cannot be empty."
            )

            return redirect(
                "post_detail",
                post_id=post.id
            )

        Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )

    return redirect(
        "post_detail",
        post_id=post.id
    )
