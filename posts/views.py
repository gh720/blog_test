import datetime
import json

import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils import dateformat as df
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, CreateView

# import django.views.generic
# django.views.generic.
from django.views.generic.detail import SingleObjectMixin

# import django
from formtools.preview import FormPreview

from django.conf import settings as defaults

from blog import settings
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment, Tag

import re


def _get_form(request, cls, prefix):
    data = request.POST if prefix + "_submit" in request.POST else None
    return cls(data)


def get_tags(request):
    tags = [{'name': str(tag), 'id': tag.pk} for tag in Tag.objects.all()]
    return JsonResponse({'items': tags})


@login_required
def remove_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(reverse('post_details', kwargs={'post_pk': post_pk}))
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
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ptags = self.object.tags.all()
        tags = [{'name': str(tag), 'id': tag.id} for tag in ptags]
        ctx['current_tags'] = json.dumps(tags)
        return ctx

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form(self.form_class)
        # form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = self.request.user
            post.updated_at = timezone.now()
            post.save()
            tags_json = self.request.POST.get('tags')
            if tags_json:
                tags = json.loads(tags_json)
                current_tags = {str(tag): tag.pk for tag in Tag.objects.all()}

                for tag_name in tags:
                    tag = None
                    if tag_name not in current_tags:
                        tag = Tag.objects.create(tag=tag_name)
                        tag.save()
                        print("created new tag: %s" % (str(tag)))
                    else:
                        tag = Tag.objects.get(tag=tag_name)
                    post.tags.add(tag)
                    print("added tag: %s" % (str(tag)))

                for tag_name in current_tags:
                    if tag_name not in tags:
                        tag = Tag.objects.get(tag=tag_name)
                        post.tags.remove(tag)
                        print("removed tag: %s" % (str(tag)))

            # form.save_m2m()
            return redirect('home')
        else:
            debug = 1
        return render(request, self.template_name, {'form': form})



    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.created_by = self.request.user
    #         post.save()
    #         form.save_m2m()
    #         return redirect('home')
    #     else:
    #         debug = 1
    #     return render(request, self.template_name, {'form': form})

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
    pk_url_kwarg = 'post_pk'
    context_object_name = 'something'

    def get_context_data(self, *, object_list=None, **kwargs):
        post_pk = self.object.pk
        ctx = super().get_context_data(**kwargs)
        ptags = self.object.tags.all()
        tags = [{'name': str(tag), 'id': tag.id} for tag in ptags]

        ctx['current_tags'] = json.dumps(tags)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        # form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = self.request.user
            post.updated_at = timezone.now()
            post.save()
            tags_json = self.request.POST.get('tags')
            if tags_json:
                tags = json.loads(tags_json)
                current_tags = {str(tag): tag.pk for tag in Tag.objects.all()}

                for tag_name in tags:
                    tag = None
                    if tag_name not in current_tags:
                        tag = Tag.objects.create(tag=tag_name)
                        tag.save()
                        print("created new tag: %s" % (str(tag)))
                    else:
                        tag = Tag.objects.get(tag=tag_name)
                    post.tags.add(tag)
                    print("added tag: %s" % (str(tag)))

                for tag_name in current_tags:
                    if tag_name not in tags:
                        tag = Tag.objects.get(tag=tag_name)
                        post.tags.remove(tag)
                        print("removed tag: %s" % (str(tag)))

            # form.save_m2m()
            return redirect('home')
        else:
            debug = 1
        return render(request, self.template_name, {'form': form})

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
            post.comment_count += 1
            post.save()
            comment = cform.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            cform = CommentForm()
            return redirect(reverse('post_details', kwargs={'post_pk': kwargs['post_pk']}));
        else:
            return render(request, 'post_details.html', {'post': post, 'comment_form': cform})

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        post.view_count += 1
        post.save()
        return super(PostDetailsView, self).get(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = ctx.get('comment_form', CommentForm())
        return ctx


class login_view_c(base_view_c, LoginView):
    pass


class password_change_view_c(base_view_c, PasswordChangeView):
    pass

class password_change_view_done_c(base_view_c, PasswordChangeDoneView):
    pass

class password_reset_view_c(base_view_c, PasswordResetView):
    email_template_name = 'pass_reset_email.html'
    subject_template_name = 'pass_reset_subject.txt'

    def get_success_url(self):
        return reverse('pass_reset_done')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class password_reset_done_view_c(base_view_c, PasswordResetDoneView):
    def get_success_url(self):
        return reverse('pass_reset_confirm')

class password_reset_confirm_view_c(base_view_c, PasswordResetConfirmView):
    def get_success_url(self):
        return reverse('pass_reset_complete')

class password_reset_complete_view_c(base_view_c, PasswordResetCompleteView):
    pass


class post_edit_form_preview_c(FormPreview):
    form_class = PostForm
    form_template = 'edit_post.html'
    preview_template = 'edit_post_preview.html'

    pk_url_kwarg = 'post_pk'

    def get_context(self, request, form):
        ctx=super().get_context(request, form)
        d = datetime.datetime.now()
        formatter = df.DateFormat(d)
        format = settings.__dict__.get('DATETIME_FORMAT', defaults.DATETIME_FORMAT)

        ctx['post_preview']={ 'created_by': request.user, 'created_at': formatter.format(format)}
        return ctx

    def done(self,request,cleaned_data):
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        # form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = self.request.user
            post.updated_at = timezone.now()
            post.save()
            tags_json = self.request.POST.get('tags')
            if tags_json:
                tags = json.loads(tags_json)
                current_tags = {str(tag): tag.pk for tag in Tag.objects.all()}

                for tag_name in tags:
                    tag = None
                    if tag_name not in current_tags:
                        tag = Tag.objects.create(tag=tag_name)
                        tag.save()
                        print("created new tag: %s" % (str(tag)))
                    else:
                        tag = Tag.objects.get(tag=tag_name)
                    post.tags.add(tag)
                    print("added tag: %s" % (str(tag)))

                for tag_name in current_tags:
                    if tag_name not in tags:
                        tag = Tag.objects.get(tag=tag_name)
                        post.tags.remove(tag)
                        print("removed tag: %s" % (str(tag)))
            return redirect('home')
        else:
            debug = 1
        return render(request, self.template_name, {'form': form})

