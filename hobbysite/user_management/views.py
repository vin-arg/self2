from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from .forms import RegisterForm, ProfileForm
from merchstore.models import Product
from wiki.models import Article as Wiki_Article
from blog.models import Article as Blog_Article
from forum.models import Thread
from commissions.models import Commission

def home_page(request):
    # Get products bought by the logged-in user
    bought_products = Product.objects.all()

    # Get products sold by the logged-in user
    sold_products = Product.objects.all()

    # Get wiki articles created by the logged-in user
    wiki_articles = Wiki_Article.objects.all()

    # Get blog articles created by the logged-in user
    blog_articles = Blog_Article.objects.all()

    # Get threads created by the logged-in user
    threads = Thread.objects.all()

    # Get commissions created by the logged-in user
    created_commissions = Commission.objects.all()

    # Get commissions the logged-in user has joined
    joined_commissions = Commission.objects.all()

    # Pass all the retrieved data to the template context
    context = {
        'bought_products': bought_products,
        'sold_products': sold_products,
        'wiki_articles': wiki_articles,
        'blog_articles': blog_articles,
        'threads': threads,
        'created_commissions': created_commissions,
        'joined_commissions': joined_commissions,
    }

    return render(request, 'home.html', context)

def profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    return render(request, 'profile.html', {'profile_form': form, 'profile': profile})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, name=user.username, email=user.email)
            login(request, user)
            return redirect('home_page')   
    return render(request, 'registration/register.html', {'regform': form})