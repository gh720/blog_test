import string

import time
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

from posts.models import Comment


@shared_task
def celery_test_task(input=None):
    time.sleep(5)
    count = Comment.objects.count()
    return  { 'count': count } # '%s Done!' % (input);
