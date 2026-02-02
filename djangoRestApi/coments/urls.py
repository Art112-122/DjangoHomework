from django.urls import path
from . import views

app_name = "coments"

urlpatterns = [
    path("", views.posts_list, name="posts"),
    path("add-comment/", views.add_comment, name="add_comment"),
    path(
        "delete-comment/<int:comment_id>/", views.delete_comment, name="delete_comment"
    ),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("dislike/<int:post_id>/", views.dislike_post, name="dislike_post"),
]
