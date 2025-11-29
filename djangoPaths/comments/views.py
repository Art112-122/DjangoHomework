from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Comment, Post



class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"]).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["post_id"] = self.kwargs["post_id"]
        return ctx


class CommentDetailView(DetailView):
    model = Comment
    template_name = "comments/comment_detail.html"
    context_object_name = "comment"


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["text"]
    template_name = "comments/comment_form.html"

    def form_valid(self, form):
        post_id = self.kwargs["post_id"]
        form.instance.post = Post.objects.get(id=post_id)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("comment_list", kwargs={"post_id": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["text"]
    template_name = "comments/comment_form.html"

    def test(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("comment_detail", kwargs={"pk": self.object.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def test(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("comment_list", kwargs={"post_id": self.object.post.id})
