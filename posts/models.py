from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    message = models.TextField(max_length=4000)
    title = models.TextField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete= models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete= models.CASCADE)


