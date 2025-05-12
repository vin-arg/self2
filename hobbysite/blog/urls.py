from django.urls import path
from .views import article_list, article_detail, article_create, article_update

urlpatterns = [
    path('articles/', article_list, name='article_list'),
    path('article/<int:num>/', article_detail, name='article_detail'),
    path('article/add/', article_create, name='article_create'),
    path('article/<int:num>/edit/', article_update, name='article_update'),

]