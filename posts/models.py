import time

import os

from PIL import Image
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse

from posts.common import user_uploads_path
from django.db.models import Q


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag


class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "tag"]


#import django.contrib.auth.backends
import django.contrib.auth
# import rules

class Post(models.Model):
    '''
    holds a post, related to :model:`posts.Post` and :model:`auth.User`
    '''

    title = models.CharField(max_length=400)
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+',
                                   on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        # db_table = 'posts_post'
        permissions = [
            ('view_post', 'Can view entry'),  # check if empty
        ]
        pass

    def __str__(self):
        # _fields = Post._meta.get_fields()
        return self.title

    def custom_order(self):
        return

    def get_absolute_url(self):
        return reverse('post_details', args=[self.pk])

    def assigned_tags(self):
        return ";".join([str(tag) for tag in self.tags.all()])


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "message", 'created_at', 'updated_at'
        , 'created_by', 'updated_by', 'view_count', 'assigned_tags', 'comment_count']
    show_full_result_count = True
    view_on_site = True


class Comment(models.Model):
    message = models.TextField(max_length=400)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:30]


class profile_c(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to=user_uploads_path, blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_thumbnail()

    def crop_box(self, width, height):
        left = upper = lower = right = 0
        if width > height:
            left = int((width - height) / 2)
            right = height + left
            lower = height
        else:
            upper = int((height - width) / 2)
            right = width
            lower = width + upper
        return (left, upper, right, lower)

    def save_thumbnail(self):
        PROFILE_IMAGE_SIZE = getattr(settings, 'PROFILE_IMAGE_SIZE', (100, 100))
        thumb_path = self.get_thumb_path()
        if not thumb_path:
            return None
        if default_storage.exists(thumb_path):
            raise FileExistsError
        f = default_storage.open(self.profile_image.name, 'rb')
        image = Image.open(f)
        width, height = image.size
        (left, upper, right, lower) = self.crop_box(width, height)
        cropped = image.crop((left, upper, right, lower))
        cropped = cropped.resize(PROFILE_IMAGE_SIZE, Image.ANTIALIAS)
        fh = default_storage.open(thumb_path, "wb")
        cropped.save(fh, "JPEG")
        fh.close()
        return True

    def get_thumb_path(self):
        if not self.profile_image:
            return None
        file_path = self.profile_image.name
        path, name = os.path.split(file_path)
        base, ext = os.path.splitext(name)
        thumb_name = "%s_thumb.jpg" % (base)
        user_path = "%s/%s/%s" % (settings.MEDIA_ROOT, path, thumb_name)
        return user_path

    def get_thumb_url(self):
        if not self.profile_image:
            return None
        file_path = self.profile_image.name
        path, name = os.path.split(file_path)
        base, ext = os.path.splitext(name)
        thumb_name = "%s_thumb.jpg" % (base)
        user_path = "%s%s/%s" % (settings.MEDIA_URL, path, thumb_name)
        return user_path

    @property
    def thumb_url(self):
        return self.get_thumb_url()
