from django.db import models
from user_management.models import Profile 

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    #sort by name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Thread Categories"

    def __str__(self):
        return self.name
    
class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ThreadCategory, null=True, blank=True, on_delete=models.SET_NULL)
    entry = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    #sort by descending date
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True) 

    #sort by ascending date
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"comment by {self.author} on {self.thread}"