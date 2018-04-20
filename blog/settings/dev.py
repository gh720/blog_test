from .base import *
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default' : DATABASE_CONFIGS['sqlite']
}

