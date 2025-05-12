from django.db import models
from django.contrib.auth.models import User


class ArticleCategory(models.Model):
    """Model representing an article category."""

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    """Model representing an article."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )
    entry = models.TextField(null=True, blank=True)
    header_image = models.ImageField(
        upload_to="article_headers/",
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} by {self.author.username if self.author else 'Unknown'}"


class Comment(models.Model):
    """Model representing a comment on an article."""

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return (
            f"Comment by {self.author.username if self.author else 'Unknown'} "
            f"on {self.article.title}"
        )


class ArticleImage(models.Model):
    """Model to render images and surrounding elements."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image = models.ImageField(upload_to='article_gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"
