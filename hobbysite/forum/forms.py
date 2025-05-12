from django import forms
from .models import Thread, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['author', 'created_on', 'updated_on']

class ThreadUpdateForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['author', 'created_on']