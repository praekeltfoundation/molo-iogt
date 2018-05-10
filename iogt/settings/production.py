from .base import *  # noqa


# Disable debug mode

DEBUG = False
TEMPLATE_DEBUG = False
ENV = 'prd'


# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE

COMPRESS_OFFLINE = True


# Send notification emails as a background task using Celery,
# to prevent this from blocking web server threads
# (requires the django-celery package):
# http://celery.readthedocs.org/en/latest/configuration.html

# import djcelery
#
# djcelery.setup_loader()
#
# CELERY_SEND_TASK_ERROR_EMAILS = True
# BROKER_URL = 'redis://'


# Use Redis as the cache backend for extra performance
# (requires the django-redis-cache package):
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#cache

# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.cache.RedisCache',
#         'LOCATION': '127.0.0.1:6379',
#         'KEY_PREFIX': 'base',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
#         }
#     }
# }


COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'ENV': ENV,
}

HTTPS_PATHS = ['admin', 'profiles/register/', 'profiles/login/']

try:
    from .local import *  # noqa
except ImportError:
    pass
