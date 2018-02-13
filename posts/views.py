from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView

from posts.forms import PostForm
from posts.models import Post

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



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

class PostEditView(UpdateView):
    model = Post
    fields=('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg='post_pk'
    context_object_name='something'

    def form_valid(self, form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        return redirect('home')
