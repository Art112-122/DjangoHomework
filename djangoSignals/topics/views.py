from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import Topic


@login_required
def topics_view(request):
    cache_key = f"user:{request.user.id}:topics"
    topics = cache.get(cache_key)

    if topics is None:
        topics = Topic.objects.prefetch_related("subscribers")
        cache.set(cache_key, topics, 60)

    return render(request, "topics/topics.html", {"topics": topics})


@login_required
def subscribe_view(request, id):
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.add(request.user)
    return redirect("topics")


@login_required
def unsubscribe_view(request, id):
    topic = get_object_or_404(Topic, id=id)
    topic.subscribers.remove(request.user)
    return redirect("topics")


@login_required
def create_topic_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Topic.objects.create(name=name)
    return redirect("topics")


@login_required
def delete_topic_view(request, id):
    topic = get_object_or_404(Topic, id=id)
    topic.delete()
    return redirect("topics")
