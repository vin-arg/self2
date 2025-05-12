from django.db import models
from django.contrib.auth.models import User
from user_management.models import Profile

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    # author = models.ForeignKey('user_management.Profile', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="art_cat")
    entry = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

class ArticleComment(models.Model):
    # author = models.ForeignKey('user_management.Profile', on_delete=models.CASCADE, null=True, blank=True) # to use if calling unto profile
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on'] 

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"

    