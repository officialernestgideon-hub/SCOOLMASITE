from django.contrib import admin

# Register your models here.

from .models import Category, Post, Like, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "university",
        "category",
        "is_verified",
        "is_published",
        "views_count",
        "created_at",
    )

    list_filter = (
        "university",
        "category",
        "is_verified",
        "is_published",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
