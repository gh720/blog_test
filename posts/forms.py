from django import forms

from posts.models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    # test = forms.MultipleChoiceField(choices=[('aaa', 'aaa'),('bbb','bbb'),('ccc','ccc')], widget=forms.CheckboxSelectMultiple(), required=False, label='test')

    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Post
        fields=('title','message')
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
