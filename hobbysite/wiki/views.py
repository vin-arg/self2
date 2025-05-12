from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ArticleForm, CommentForm
from .models import Article, ArticleCategory


@login_required
def article_create_view(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("wiki:article_detail", pk=article.pk)
    else:
        form = ArticleForm()

    return render(
        request,
        "wiki/article_form.html",
        {"article_form": form, "is_create": True}
    )


@login_required
def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        return redirect("wiki:article_detail", pk=article.pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect("wiki:article_detail", pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "wiki/article_form.html",
        {"article_form": form, "is_create": False}
    )


def article_list_view(request):
    all_articles = Article.objects.all()
    categories = ArticleCategory.objects.prefetch_related(
        'articles'
    ).all()

    user_articles = Article.objects.none()
    if request.user.is_authenticated:
        user_articles = all_articles.filter(author=request.user)
        all_articles = all_articles.exclude(author=request.user)

    category_articles = {}
    for category in categories:
        if request.user.is_authenticated:
            articles_in_category = category.articles.exclude(
                author=request.user
            )
        else:
            articles_in_category = category.articles.all()

        if articles_in_category.exists():
            category_articles[category] = articles_in_category

    return render(
        request,
        "wiki/article_list.html",
        {
            "user_articles": user_articles,
            "category_articles": category_articles
        }
    )


def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    gallery_images = article.gallery_images.all()
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(pk=article.pk)[:2]

    comment_form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.article = article
                comment.save()
                return redirect("wiki:article_detail", pk=pk)
        else:
            comment_form = CommentForm()

    comments = article.comments.all().order_by("-created_on")

    return render(
        request,
        "wiki/article_detail.html",
        {
            "article": article,
            "related_articles": related_articles,
            "comments": comments,
            "comment_form": comment_form,
            "gallery_images": gallery_images
        }
    )
