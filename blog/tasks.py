import string

import time
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def celery_test_task(input):
    time.sleep(5)
    return '%s Done!' % (input);
