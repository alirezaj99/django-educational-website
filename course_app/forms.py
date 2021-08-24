from django import forms
from .models import Comment
from extensions.utils import ModelFormWithRecaptcha


class CommentForm(ModelFormWithRecaptcha):
    class Meta:
        model = Comment
        fields = ['message']
