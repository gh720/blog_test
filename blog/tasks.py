import string

import time
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

from posts.models import Comment


@shared_task
def celery_test_task(post_pk=None):
    time.sleep(3) # emulating delay
    count = Comment.objects.filter(post__pk=post_pk).count()
    return  { 'count': count } # '%s Done!' % (input);
