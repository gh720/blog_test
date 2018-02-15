from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=400)
    message = models.TextField(max_length=4000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete= models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    message = models.TextField(max_length=400)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete= models.CASCADE)

