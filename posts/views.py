from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView
# import django.views.generic
# django.views.generic.
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment

def _get_form(request, cls, prefix):
    data = request.POST if prefix+"_submit" in request.POST else None
    return cls(data)


@login_required
def new_post(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.created_by=request.user
            post.save()
            return redirect(reverse('home'))
    else:
        form=PostForm()
    return render(request, 'new_post.html', { 'form':form })


@login_required
def new_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.created_by=request.user
            comment.save()
            return redirect(reverse('post_details', kwargs={ 'post_pk': post.pk }))
        else:
            return redirect(reverse('post_details', kwargs={'post_pk': post.pk }), { 'form':form  })
            # return render(request, 'post_details.html', { 'post':post, 'form': form})

@login_required
def remove_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(reverse('post_details', kwargs={ 'post_pk': post_pk }))
            # return render(request, 'post_details.html', { 'post':post, 'form': form})

@login_required
def remove_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect(reverse('home'))

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'



class PostDetailsView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_details.html'
    pk_url_kwarg = 'post_pk'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        cform = _get_form(request, CommentForm, 'comment')
        if cform.is_bound and cform.is_valid():
            comment=cform.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            cform = CommentForm()
        return render(request, 'post_details.html', {'post': post, 'comment_form': cform })

    def get_context_data(self, **kwargs):
        ctx = super(PostDetailsView, self).get_context_data(**kwargs)
        ctx['comment_form']=ctx.get('comment_form', CommentForm())
        return ctx


class PostEditView(UpdateView):
    model = Post
    fields=('title','message',)
    template_name = 'edit_post.html'
    pk_url_kwarg='post_pk'
    context_object_name='something'

    def form_valid(self, form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        post.save()
        return redirect('home')
