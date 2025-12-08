from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm


def article_list(request):
    qs = Article.objects.select_related("author").order_by("-created_at")
    paginator = Paginator(qs, 5)  # 5 на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "articles/list.html", {"page_obj": page_obj})


@login_required
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("articles:list")
    else:
        form = ArticleForm()

    return render(request, "articles/create.html", {"form": form})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "articles/detail.html", {"article": article})
