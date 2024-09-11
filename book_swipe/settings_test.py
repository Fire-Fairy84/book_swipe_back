# settings_test.py
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'book_swipe_test',
        'USER': 'postgres',
        'PASSWORD': '1321',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DEBUG = False
