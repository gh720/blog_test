import datetime
import json

import logging

import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils import dateformat as df
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, CreateView, TemplateView
from django.core import serializers
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import rules.contrib.views as rviews
from formtools.preview import FormPreview

from django.conf import settings as defaults

from blog import settings
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment, Tag

logger = logging.getLogger('blog')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


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


class base_view_c():
    def add_common_context(self, ctx):
        last3 = Post.objects.all().order_by('-created_at')[:3]
        popular3 = Post.objects.all().order_by('-comment_count')[:3]
        ctx['latest_posts'] = last3
        ctx['popular_posts'] = popular3
        ctx['tags'] = Tag.objects.all()
        # try:
        #     obj = super().get_object()
        #     ctx['can_edit'] = self.can_edit(obj)
        # except AttributeError:
        #     pass
        return ctx

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return self.add_common_context(ctx)

    def get_context(self, request, form):
        ctx = super().get_context(request, form)
        return self.add_common_context(ctx)

    def can_edit(self, obj):
        if not obj:
            return False
        if not (self.request.user and self.request.user.is_authenticated):
            return False
        if obj.created_by == self.request.user:
            return True
        if self.request.user.is_superuser:
            return True
        if hasattr(self, 'has_permission') and self.has_permission():
            return True
        return False


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




class post_list_view_c(base_view_c, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

class tags_view_c(base_view_c, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

    pk_kw_arg = 'tag_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        tag = self.request.resolver_match.kwargs.get(self.pk_kw_arg)
        if tag:
            try:
                ctx['heading'] = 'Posts for "%s"' % (Tag.objects.get(id=int(tag)))
            except Exception as e:
                logger.error(str(e))
        return ctx

    def get_queryset(self):
        tag = self.request.resolver_match.kwargs.get(self.pk_kw_arg)
        result = None
        if tag:
            result = Post.objects.filter(tags=tag)
        else:
            result = Post.objects.all()
        return result


class post_details_view_c(base_view_c, DetailView):
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
            return redirect(reverse('post_details', kwargs={'post_pk': kwargs['post_pk']}))
        else:
            return render(request, 'post_details.html', {'post': post, 'comment_form': cform})

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        post.view_count += 1
        post.save()
        return super(post_details_view_c, self).get(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = ctx.get('comment_form', CommentForm())
        return ctx


####### edit views

class post_create_view_c(base_view_c, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # fields = ('title', 'message', 'tags')
    initial = dict()
    template_name = 'new_post.html'
    pk_url_kwarg = 'post_pk'
    permission_required = [ 'post.add', ]

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
            post.created_by = self.request.user
            post.created_at = timezone.now()
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



class post_edit_view_c(base_view_c, rviews.PermissionRequiredMixin, UpdateView):
    model = Post
    permission_required = [ 'post.change', ]
    form_class = PostForm

    def get_permission_object(self):
        return super().get_permission_object()

    # fields=('title','message','tags')
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'something'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # if self.can_edit(obj):
        #     return obj
        return obj
        # raise Http404

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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


class post_edit_form_preview_c(base_view_c, SingleObjectMixin, rviews.PermissionRequiredMixin, FormPreview):
    form_class = PostForm
    permission_required = 'post.change'
    form_template = 'edit_post.html'
    preview_template = 'edit_post_preview.html'

    pk_url_kwarg = 'post_pk'

    def parse_params(self, request, *args, **kwargs):
        super().parse_params(request, *args, **kwargs)
        if 'post_pk' in kwargs:
            self.state['post_pk'] = kwargs['post_pk']

    def get_initial(self, request):
        initial = super().get_initial(request)
        initial['pk'] = self.state['post_pk']
        return initial

    def get_queryset(self):
        return Post.objects

    def preview_get(self, request):
        self.request = request
        self.kwargs = request.resolver_match.kwargs
        self.object = self.get_object()
        # if 'post_pk' in request.resolver_match.kwargs:
        #     self.object = Post.objects.get(pk=request.resolver_match.kwargs['post_pk'])
        if not self.has_permission():
            return self.handle_no_permission()

        f = self.form(auto_id=self.get_auto_id(),
                      initial=self.get_initial(request), instance=self.object)
        return render(request, self.form_template, self.get_context(request, f))

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        return super().has_permission()

    def get_context(self, request, form):
        ctx = super().get_context(request, form)
        d = datetime.datetime.now()
        formatter = df.DateFormat(d)
        format = settings.__dict__.get('DATETIME_FORMAT', defaults.DATETIME_FORMAT)

        ctx['post_preview'] = {'created_by': request.user, 'created_at': formatter.format(format)}
        return ctx

    def done(self, request, cleaned_data):
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


######### ajax

class comment_json_c(DetailView):
    model = Post
    pk_url_kwarg = 'post_pk'

    def render_to_response(self, context, **response_kwargs):
        if 0 and not self.request.is_ajax():
            return Http404
        qs = Comment.objects.all()[0]
        obj = serializers.serialize('json', [qs])
        return HttpResponse(obj, content_type='application/json')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class comment_refresh_json_c(DetailView):
    model = Post
    pk_url_kwarg = 'post_pk'

    def render_to_response(self, context, **response_kwargs):
        if 0 and not self.request.is_ajax():
            raise Http404
        count = Comment.objects.count()
        # obj = serializers.serialize('json', )
        raise Http404
        #return JsonResponse({ 'count': count })
        # return HttpResponse(obj, content_type='application/json')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def get_post_comments_async(request, post_pk):
    qs = Comment.objects.filter(post__pk=post_pk)
    if request.is_ajax():
        return JsonResponse(qs)
    else:
        return Http404
    tags = [{'name': str(tag), 'id': tag.pk} for tag in Tag.objects.all()]
    return JsonResponse({'items': tags})
