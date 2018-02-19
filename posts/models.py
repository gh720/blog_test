import time
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from posts.common import user_uploads_path


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.tag);

class Post(models.Model):
    title = models.CharField(max_length=400)
    message = models.TextField(max_length=4000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+', on_delete= models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_details', args=[self.pk])

class Comment(models.Model):
    message = models.TextField(max_length=400)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+', on_delete= models.CASCADE)

class profile_c(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to=user_uploads_path,blank=True, null=True)
    class Meta:
        verbose_name="profile"
        verbose_name_plural="profiles"
