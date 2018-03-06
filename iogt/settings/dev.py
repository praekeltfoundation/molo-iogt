from .base import *  # noqa


DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = 'amqp://rabbit:secret@rabbitmq.com:5672/molo-iogt'


try:
    from .local import *  # noqa
except ImportError:
    pass
