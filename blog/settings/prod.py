from .base import *

DEBUG = False
# DEBUG = True

ADMINS = (
    ('ME', 'webmaster@test.local'),
)

# to make this secure, replace '*' with the hostname of the server running Django
ALLOWED_HOSTS = ['*','localhost', '127.0.0.1']

DATABASES = {
    'default' : DATABASE_CONFIGS['postgresql']
}

