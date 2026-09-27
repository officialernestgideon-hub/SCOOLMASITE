from django.urls import path

from . import views


urlpatterns = [
    path(
        "create/",
        views.create_post,
        name="create_post"
    ),
    
    path(
        "<int:post_id>/",
        views.post_detail,
        name="post_detail"
    ),

    path(
        "<int:post_id>/like/",
        views.like_post,
        name="like_post"
    ),

    path(
        "<int:post_id>/comment/",
        views.add_comment,
        name="add_comment"
    ),
]