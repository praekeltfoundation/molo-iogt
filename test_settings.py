from iogt.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'iogt_test.db',
    }
}

DEBUG = True
CELERY_ALWAYS_EAGER = True
