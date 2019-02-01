from .default import *
import os

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgress'),
        'USER': os.environ.get('POSTGRES_USER', 'postgress'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'root'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}
