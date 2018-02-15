from django import forms

from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    test = forms.MultipleChoiceField(choices=['aaa','bbb','ccc'], widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model=Post
        fields=('title','message', 'tags')
        labels=dict()

class CommentForm(forms.ModelForm):
    prefix = 'comment'
    class Meta:
        model=Comment
        fields=('message',)
        labels = {
            'message' : 'Your comment:'
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }