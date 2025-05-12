from django.contrib import admin
from .models import ArticleCategory, Article


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for ArticleCategory model."""
    list_display = ("name", "description")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model."""
    list_display = ("title", "category", "created_on", "updated_on")
    list_filter = ("category", "created_on")
    search_fields = ("title", "entry")
