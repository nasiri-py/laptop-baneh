from django import forms
from .models import Comment, Compare


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class CompareForm(forms.ModelForm):
    class Meta:
        model = Compare
        fields = ['product']
