from django.contrib import admin
from .models import ArticleCategory, Article, ArticleComment


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on',)
    search_fields = ('title', 'entry',)
    list_filter = ('category', 'created_on',)

class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_on', 'updated_on')
    search_fields = ('entry', 'author__name', 'article__title')
    list_filter = ('created_on', 'article')

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.register(ArticleComment, ArticleCommentAdmin)
