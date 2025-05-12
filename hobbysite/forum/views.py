from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import Thread, ThreadCategory, Comment
from .forms import ThreadForm, ThreadUpdateForm, CommentForm
from user_management.models import Profile


def thread_list(request):
    threads = Thread.objects.select_related('category', 'author').all()
    categories = ThreadCategory.objects.all()

    user_threads = None
    grouped_threads = defaultdict(list)

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_threads = threads.filter(author=request.user.profile)
        others = threads.exclude(author=request.user.profile)
    else:
        others = threads

    for thread in others:
        grouped_threads[thread.category].append(thread)

    return render(request, 'forum/thread_list.html', {
        'user_threads': user_threads,
        'grouped_threads': dict(grouped_threads),
        'categories': categories,
        'selected_category': None,
    })


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, id=pk)
    related_threads = Thread.objects.filter(category=thread.category).exclude(pk=thread.pk)[:2]
    comments = Comment.objects.filter(thread=thread).order_by('created_on')

    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.thread = thread
                comment.author = request.user.profile
                comment.save()
                return redirect('forum:thread_detail', pk=thread.pk)
        else:
            form = CommentForm()

    is_owner = request.user.is_authenticated and request.user.profile == thread.author

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'related_threads': related_threads,
        'comments': comments,
        'form': form,
        'is_owner': is_owner,
    })

@login_required
def thread_create(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    thread_form = ThreadForm(request.POST or None, request.FILES or None)
    if thread_form.is_valid():
        thread = thread_form.save(commit=False)
        thread.author = request.user.profile  
        thread.save()
        return redirect('forum:thread_detail', pk=thread.pk)

    return render(request, 'forum/thread_form.html', {'form': thread_form})


@login_required
def thread_update(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    if thread.author != request.user.profile:
        return redirect('forum:thread_detail', pk=pk)

    if request.method == 'POST':
        form = ThreadUpdateForm(request.POST, request.FILES, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum:thread_detail', pk=pk)
    else:
        form = ThreadUpdateForm(instance=thread)

    return render(request, 'forum/thread_form.html', {
        'form': form,
        'is_update': True
    })


def threads_by_category(request, category_id):
    category = get_object_or_404(ThreadCategory, id=category_id)
    threads = Thread.objects.filter(category=category)
    return render(request, "forum/thread_list.html", {
        "threads": threads,
        "selected_category": category
    })
