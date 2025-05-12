from django.urls import path
from . import views
from django.shortcuts import redirect


app_name = "forum"

urlpatterns = [
    path("threads/", views.thread_list, name="thread_list"),
    path("thread/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("category/<int:category_id>/", views.threads_by_category, name="threads_by_category"),  
    path("thread/add/", views.thread_create, name="thread_create"),
    path("threads/<int:pk>/edit/", views.thread_update, name="thread_update"),
]
