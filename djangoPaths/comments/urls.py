from django.urls import path
from .views import (
    CommentListView,
    CommentDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="comment_list"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path("posts/<int:post_id>/comments/create/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
