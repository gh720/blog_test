from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.tag);

class Post(models.Model):
    title = models.CharField(max_length=400)
    message = models.TextField(max_length=4000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete= models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_details', args=[self.pk])

class Comment(models.Model):
    message = models.TextField(max_length=400)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete= models.CASCADE)

