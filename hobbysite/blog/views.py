from django.shortcuts import render, redirect
from django.db.models import Prefetch
from .models import Article, ArticleCategory, ArticleComment
from .forms import ArticleForm, ArticleCategoryForm, ArticleUpdateForm, ArticleCommentForm
from django.contrib.auth.decorators import login_required

def article_list(request):
    user_profile = request.user.profile
    articles_by_user = Article.objects.filter(author=user_profile)
    categories = ArticleCategory.objects.prefetch_related(
        Prefetch('art_cat', queryset=Article.objects.exclude(author=user_profile))
    )
    articles = Article.objects.exclude(author=user_profile)

    return render(request,'article_list.html',{'articles': articles,'categories': categories,'articles_by_user': articles_by_user,})

def article_detail(request, num=1):
    article = Article.objects.filter(pk=num).first()
    comments = ArticleComment.objects.filter(article=article)
    related_articles = Article.objects.filter(author=article.author).exclude(pk=num)
    
    if request.method == "POST":
        comment_form = ArticleCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            comment.article = article
            if request.user.is_authenticated:
                comment.author = request.user.profile  # Set the author to the user's profile
            comment.save()
            return redirect('article_detail', num=article.pk)

    comment_form = ArticleCommentForm()

    
    return render(request, 'article_detail.html', {'article': article, 'comments': comments, 'comment_form': comment_form, 'related_articles': related_articles,})

def article_create(request):
    
    if (request.method == "POST"):
        form = ArticleForm(request.POST, request.FILES)
        category_form = ArticleCategoryForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            return redirect('article_list')

        if category_form.is_valid():
            category_form.save()
            return redirect('article_list')
        
    form = ArticleForm()
    category_form = ArticleCategoryForm()

    return render(request, 'article_create.html', {'article_form': form, 'category_form': category_form})

def article_update(request, num=1):
    article = Article.objects.filter(pk=num).first()
    
    if not article:
        return redirect('article_list') 

    if request.method == 'POST':
        form = ArticleUpdateForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', num=article.pk)
    else:
        form = ArticleUpdateForm(instance=article)

    return render(request, 'article_update.html', {'article': article, 'update_form': form})
