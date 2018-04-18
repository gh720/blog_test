from .base import *

DEBUG = False

ADMINS = (
    ('ME', 'webmaster@test.local'),
)

ALLOWED_HOSTS = ['192.168.99.100','127.0.0.1','dockr']

DATABASES = {
    'default' : DATABASE_CONFIGS['postgresql']
}
