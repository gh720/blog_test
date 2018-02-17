from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, CreateView
# import django.views.generic
# django.views.generic.
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment

def _get_form(request, cls, prefix):
    data = request.POST if prefix+"_submit" in request.POST else None
    return cls(data)




# @login_required
# def new_comment(request, post_pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     if request.method=='POST':
#         form=CommentForm(request.POST)
#         if form.is_valid():
#             comment=form.save(commit=False)
#             comment.post=post
#             comment.created_by=request.user
#             comment.save()
#             return redirect(reverse('post_details', kwargs={ 'post_pk': post.pk }))
#         else:
#             return redirect(reverse('post_details', kwargs={'post_pk': post.pk }), { 'form':form  })
#             # return render(request, 'post_details.html', { 'post':post, 'form': form})

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

class base_view_c:
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        last3 = Post.objects.all().order_by('-created_at')[:3]
        popular3 = Post.objects.all().order_by('-comment_count')[:3]
        ctx['latest_posts'] = last3
        ctx['popular_posts'] = popular3
        return ctx

# @login_required
# def new_post(request):
#     if request.method=='POST':
#         form=PostForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.created_by=request.user
#             post.save()
#             return redirect(reverse('home'))
#     else:
#         form=PostForm()
#     return render(request, 'new_post.html', { 'form':form })

class post_create_view_c(base_view_c, CreateView):
    model = Post
    form_class = PostForm
    # fields = ('title', 'message', 'tags')
    initial = dict()
    template_name = 'new_post.html'
    pk_url_kwarg = 'post_pk'
    # context_object_name = 'something'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request,self.template_name, {'form':form})

    def post(self,  request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = self.request.user
            post.save()
            form.save_m2m()
            return redirect('home')
        else:
            debug=1
        return render(request, self.template_name, {'form': form})

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.created_by = self.request.user
    #     post.save()
    #     return redirect('home')


class PostEditView(base_view_c, UpdateView):
    model = Post
    form_class = PostForm

    # fields=('title','message','tags')
    template_name = 'edit_post.html'
    pk_url_kwarg='post_pk'
    context_object_name='something'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        # form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = self.request.user
            post.updated_at = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('home')
        else:
            debug = 1
        return render(request, self.template_name, {'form': form})

    # def form_valid(self, form):
    #     post=form.save(commit=False)
    #     post.updated_by=self.request.user
    #     post.updated_at=timezone.now()
    #     post.save()
    #     return redirect('home')


class PostListView(base_view_c, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

class PostDetailsView(base_view_c, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_details.html'
    pk_url_kwarg = 'post_pk'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        cform = _get_form(request, CommentForm, 'comment')
        if cform.is_bound and cform.is_valid():
            post.comment_count+=1
            post.save()
            comment=cform.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            cform = CommentForm()
        return render(request, 'post_details.html', {'post': post, 'comment_form': cform })

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        post.view_count+=1
        post.save()
        return super(PostDetailsView,self).get(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form']=ctx.get('comment_form', CommentForm())
        return ctx


class login_view_c(base_view_c, LoginView):
    pass
