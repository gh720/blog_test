from django import forms

from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','message',)

class CommentForm(forms.ModelForm):
    prefix = 'comment'
    class Meta:
        model=Comment
        fields=('message',)