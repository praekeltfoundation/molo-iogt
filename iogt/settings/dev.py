from .base import *  # noqa


DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = 'amqp://rabbit:secret@rabbitmq.com:5672/molo-iogt'

ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', '127.0.0.1').split(",")

try:
    from .local import *  # noqa
except ImportError:
    pass
