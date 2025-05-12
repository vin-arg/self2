from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["author", "created_on", "updated_on"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["entry"]
        widgets = {
            "entry": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Leave a comment? Share your thoughts!"
                    )
                }
            )
        }
