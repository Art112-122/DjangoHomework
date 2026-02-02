from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Post, Comment


def posts_list(request):
    posts = Post.objects.prefetch_related("comment_set")
    return render(request, "myapp/posts.html", {"posts": posts})


@require_POST
def add_comment(request):
    post_id = request.POST.get("post_id")
    text = request.POST.get("text")

    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(post=post, text=text)

    return JsonResponse(
        {
            "id": comment.id,
            "text": comment.text,
            "comments_count": post.comment_set.count(),
        }
    )


@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    comment.delete()

    return JsonResponse({"comments_count": post.comment_set.count()})


@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()

    return JsonResponse({"likes": post.likes})


@require_POST
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes += 1
    post.save()

    return JsonResponse({"dislikes": post.dislikes})
