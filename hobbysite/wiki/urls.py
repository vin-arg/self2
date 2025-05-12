from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    article_list_view, article_detail_view,
    article_create_view, article_update_view,
)

urlpatterns = [
    path("articles/", article_list_view, name="articles"),
    path("article/<int:pk>/", article_detail_view, name="article_detail"),
    path("article/create/", article_create_view, name="article_create"),
    path("article/add", article_create_view, name="article_create"),
    path("article/<int:pk>/edit/", article_update_view, name="article_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "wiki"
