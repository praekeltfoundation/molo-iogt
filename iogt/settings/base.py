# -*- coding: utf-8 -*-
"""
Django settings for base iogt.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from os.path import abspath, dirname, join
from os import environ
import django.conf.locale
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _
import dj_database_url
import djcelery
from celery.schedules import crontab
djcelery.setup_loader()
# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "llk8#8zc+@9d6m8ln7%azsg)do5^v24rb!0s^^!-t3tn*#r93y"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENV = 'dev'


ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', '*').split(",")


# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or
# a trailing slash
BASE_URL = 'http://example.com'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',

    'taggit',
    'modelcluster',

    'iogt',
    'molo.core',
    'molo.profiles',
    'google_analytics',
    'molo.usermetadata',
    'molo.surveys',
    'django_comments',
    'molo.commenting',
    'molo.polls',
    'wagtail_personalisation',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtailmedia',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtailsurveys',
    'wagtail.contrib.wagtailsitemaps',

    'mptt',
    'raven.contrib.django.raven_compat',
    'djcelery',
    'django_cas_ng',
    'compressor',
    'storages'
]

COMMENTS_APP = 'molo.commenting'
COMMENTS_FLAG_THRESHHOLD = 3
COMMENTS_HIDE_REMOVED = False
SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'iogt.middleware.SSLRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'molo.core.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',

    'molo.core.middleware.AdminLocaleMiddleware',
    'molo.core.middleware.NoScriptGASessionMiddleware',
    'iogt.middleware.IogtMoloGoogleAnalyticsMiddleware',
    'iogt.middleware.FaceBookPixelHistoryCounter',
    'molo.core.middleware.MultiSiteRedirectToHomepage',
    'molo.core.middleware.MaintenanceModeMiddleware',
    'molo.usermetadata.middleware.PersonaMiddleware',
    'iogt.middleware.ReferrerPolicyMiddleware',
]

# Template configuration

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['iogt/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
                'molo.core.context_processors.locale',
                'iogt.processors.compress_settings',
            ],
        },
    },
]

ROOT_URLCONF = 'iogt.urls'
WSGI_APPLICATION = 'iogt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# SQLite (simplest install)
DATABASES = {'default': dj_database_url.config(
    default='sqlite:///%s' % (join(PROJECT_ROOT, 'db.sqlite3'),))}

# PostgreSQL (Recommended, but requires the psycopg2 library and Postgresql
#             development headers)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'base',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': '',  # Set to empty string for localhost.
#         'PORT': '',  # Set to empty string for default.
#         # number of seconds database connections should persist for
#         'CONN_MAX_AGE': 600,
#     }
# }
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
CELERY_IMPORTS = (
    'molo.core.tasks', 'google_analytics.tasks', 'molo.profiles.task',
    'molo.commenting.tasks')
BROKER_URL = environ.get('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERYBEAT_SCHEDULE = {
    'rotate_content': {
        'task': 'molo.core.tasks.rotate_content',
        'schedule': crontab(minute=0),
    },
    'molo_consolidated_minute_task': {
        'task': 'molo.core.tasks.molo_consolidated_minute_task',
        'schedule': crontab(minute='*'),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = environ.get('LANGUAGE_CODE', 'en')
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Native South African languages are currently not included in the default
# list of languges in django
# https://github.com/django/django/blob/master/django/conf/global_settings.py#L50
LANGUAGES = global_settings.LANGUAGES + [
    ('zu', 'Zulu'),
    ('xh', 'Xhosa'),
    ('st', 'Sotho'),
    ('ve', 'Venda'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('rw', 'Kinyarwanda'),
    ('ss', 'Swati'),
    ('nr', 'Ndebele'),
    ('wo', 'Wolof'),
    ('yo', 'Yoruba'),
    ('ig', 'Igbo'),
    ('ha', 'Hausa'),
    ('am', 'Amharic'),
    ('ms', 'Malay'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('fil', 'Filipino'),
    ('nqo', 'N\'ko'),
    ('sys', 'Syriac'),
    ('dv', 'Dhivehi'),
    ('ber', 'Berber'),
    ('ku', 'Kurdish'),
    ('arc', 'Aramaic'),
    ('ht', 'Creole Haitian'),
    ('ky', 'Kyrgyz'),
    ('id', 'Bahasa'),
    ('my', 'Burmese'),
    ('tg', 'Tajik'),
    ('ay', 'Aymara'),
    ('qu', 'Quechua'),
    ('rn', 'Kirundi'),
    ('pt-mz', 'Portuguese Mozambique'),
    ('lg', 'Ganda'),
    ('si', 'Sinhalese'),
    ('ps', 'Pashto'),
    ('fa', 'Dari'),
]

EXTRA_LANG_INFO = {
    'zu': {
        'bidi': False,
        'code': 'zu',
        'name': 'Zulu',
        'name_local': 'Zulu'
    },
    'xh': {
        'bidi': False,
        'code': 'xh',
        'name': 'Xhosa',
        'name_local': 'Xhosa'
    },
    'st': {
        'bidi': False,
        'code': 'st',
        'name': 'Sotho',
        'name_local': 'Sotho'
    },
    've': {
        'bidi': False,
        'code': 've',
        'name': 'Venda',
        'name_local': 'Venda'
    },
    'tn': {
        'bidi': False,
        'code': 'tn',
        'name': 'Tswana',
        'name_local': 'Tswana'
    },
    'ts': {
        'bidi': False,
        'code': 'ts',
        'name': 'Tsonga',
        'name_local': 'Tsonga'
    },
    'rw': {
        'bidi': False,
        'code': 'rw',
        'name': 'Kinyarwanda',
        'name_local': 'Kinyarwanda'
    },
    'ss': {
        'bidi': False,
        'code': 'ss',
        'name': 'Swati',
        'name_local': 'Swati'
    },
    'nr': {
        'bidi': False,
        'code': 'nr',
        'name': 'Ndebele',
        'name_local': 'Ndebele'
    },
    'wo': {
        'bidi': False,
        'code': 'wo',
        'name': 'Wolof',
        'name_local': 'Wolof'
    },
    'yo': {
        'bidi': False,
        'code': 'yo',
        'name': 'Yoruba',
        'name_local': 'Yorùbá'
    },
    'ig': {
        'bidi': False,
        'code': 'ig',
        'name': 'Igbo',
        'name_local': 'Igbo'
    },
    'ha': {
        'bidi': False,
        'code': 'ha',
        'name': 'Hausa',
        'name_local': 'Hausa'
    },
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'አማርኛ'
    },
    'ms': {
        'bidi': False,
        'code': 'ms',
        'name': 'Malay',
        'name_local': 'Malaysia'
    },
    'gn': {
        'bidi': False,
        'code': 'gn',
        'name': 'Guarani',
        'name_local': 'Karaiñe’ême'
    },
    'gu': {
        'bidi': False,
        'code': 'gu',
        'name': 'Gujarati',
        'name_local': 'ગુજરાતી'
    },
    'fil': {
        'bidi': False,
        'code': 'fil',
        'name': 'Filipino',
        'name_local': 'Filipino'
    },
    'nqo': {
        'bidi': False,
        'code': 'nqo',
        'name': 'N\'ko',
        'name_local': 'N\'ko'
    },
    'sys': {
        'bidi': True,
        'code': 'sys',
        'name': 'Syriac',
        'name_local': 'ગુજરાતી'
    },
    'dv': {
        'bidi': False,
        'code': 'dv',
        'name': 'Dhivehi',
        'name_local': 'Dhivehi'
    },
    'ber': {
        'bidi': False,
        'code': 'ber',
        'name': 'Berber',
        'name_local': 'Tamaziɣt'
    },
    'ku': {
        'bidi': True,
        'code': 'ku',
        'name': 'Kurdish',
        'name_local': 'Kurdî'
    },
    'arc': {
        'bidi': True,
        'code': 'arc',
        'name': 'Aramaic',
        'name_local': 'ܐܪܡܝܐ‎'
    },
    'ht': {
        'bidi': False,
        'code': 'kr',
        'name': 'Creole Haitian',
        'name_local': 'Kreyòl ayisyen'
    },
    'ky': {
        'bidi': False,
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': 'Kreyòl ayisyen'
    },
    'id': {
        'bidi': False,
        'code': 'id',
        'name': 'Bahasa',
        'name_local': 'Bahasa'
    },
    'my': {
        'bidi': False,
        'code': 'bur_MM',
        'name': 'Burmese',
        'name_local': 'Burmese'
    },
    'tg': {
        'bidi': False,
        'code': 'tg',
        'name': 'Tajik',
        'name_local': 'тоҷикӣ'
    },
    'ay': {
        'bidi': False,
        'code': 'ay',
        'name': 'Aymara',
        'name_local': 'aymar aru'
    },
    'qu': {
        'bidi': False,
        'code': 'qu',
        'name': 'Quechua',
        'name_local': 'Kichwa'
    },
    'rn': {
        'bidi': False,
        'code': 'rn',
        'name': 'Kirundi',
        'name_local': 'Ikirundi'
    },
    'pt-mz': {
        'bidi': False,
        'code': 'pt-mz',
        'name': 'Portuguese Mozambique',
        'name_local': 'Portuguese Moçambique'
    },
    'lg': {
        'bidi': False,
        'code': 'lg',
        'name': 'Ganda',
        'name_local': 'Luganda'
    },
    'si': {
        'bidi': False,
        'code': 'si',
        'name': 'Sinhalese',
        'name_local': 'සිංහල'
    },
    'ps': {
        'bidi': False,
        'code': 'ps',
        'name': 'Pashto',
        'name_local': 'پښتو'
    },
    'fa': {
        'bidi': False,
        'code': 'fa',
        'name': 'Dari',
        'name_local': 'دری,'
    },
}

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LOCALE_PATHS = [
    join(PROJECT_ROOT, "locale"),
]

# Additional strings that need translations

_("January")
_("February")
_("March")
_("April")
_("May")
_("June")
_("July")
_("August")
_("September")
_("October")
_("November")
_("December")
_("Add anonymously")

_("This field is required")
_("Ensure this value has at least 4 characters (it has 1)")
_("Type your comment here")
_('Enter a valid phone number.')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
COMPRESS_ENABLED = True

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
WAGTAILMEDIA_MEDIA_MODEL = 'core.MoloMedia'

# Wagtail settings
LOGIN_URL = 'molo.profiles:auth_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

SITE_NAME = environ.get('SITE_NAME', "IoGT")
WAGTAIL_SITE_NAME = SITE_NAME

# Use Elasticsearch as the search backend for extra performance and better
# search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/
#     search/backends.html#elasticsearch-backend
#

ES_HOST = environ.get('ES_HOST')
ES_INDEX = environ.get('ES_INDEX')
ES_VERSION = int(environ.get('ES_VERSION', 5))

ES_BACKEND_V1 = 'gem.wagtailsearch.backends.elasticsearch'
ES_BACKEND_V2 = 'gem.wagtailsearch.backends.elasticsearch2'
ES_BACKEND_V5 = 'gem.wagtailsearch.backends.elasticsearch5'

if ES_VERSION == 5:
    SELECTED_ES_BACKEND = ES_BACKEND_V5
elif ES_VERSION == 2:
    SELECTED_ES_BACKEND = ES_BACKEND_V2
else:
    SELECTED_ES_BACKEND = ES_BACKEND_V1

ES_SELECTED_INDEX = ES_INDEX or environ.get('MARATHON_APP_ID', '')

if ES_HOST and ES_SELECTED_INDEX:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': SELECTED_ES_BACKEND,
            'URLS': [ES_HOST],
            'INDEX': ES_SELECTED_INDEX.replace('/', '')
        },
    }

# Whether to use face/feature detection to improve image
# cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

ENABLE_SSO = False

UNICORE_DISTRIBUTE_API = ''

ADMIN_LANGUAGE_CODE = environ.get('ADMIN_LANGUAGE_CODE', "en")

FROM_EMAIL = environ.get('FROM_EMAIL', "support@moloproject.org")
CONTENT_IMPORT_SUBJECT = environ.get(
    'CONTENT_IMPORT_SUBJECT', 'Molo Content Import')

CUSTOM_UIP_HEADER = 'HTTP_X_IORG_FBS_UIP'

GOOGLE_ANALYTICS = {}
GOOGLE_ANALYTICS_IGNORE_PATH = [
    # health check used by marathon
    '/health/',
    '/health_iogt/',
    # admin interfaces for wagtail and django
    '/admin/', '/django-admin/',
    # Universal Core content import URL
    '/import/',
    # browser troll paths
    '/favicon.ico', '/robots.txt',
    # when using nginx, we handle statics and media
    # but including them here just incase
    '/media/', '/static/',
    # metrics URL used by promethius monitoring system
    '/metrics',
    # REST API
    '/api/',
    # PWA serviceworker
    '/serviceworker.js',
]

GOOGLE_ANALYTICS_AGE_KEY = environ.get('GOOGLE_ANALYTICS_AGE_KEY', 'cd1')
GOOGLE_ANALYTICS_GENDER_KEY = environ.get('GOOGLE_ANALYTICS_GENDER_KEY', 'cd2')

CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH = environ.get(
    'GOOGLE_ANALYTICS_IGNORE_PATH')
if CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH:
    GOOGLE_ANALYTICS_IGNORE_PATH += [
        d.strip() for d in CUSTOM_GOOGLE_ANALYTICS_IGNORE_PATH.split(',')]

CSRF_FAILURE_VIEW = 'molo.core.views.csrf_failure'

FREE_BASICS_URL_FOR_CSRF_MESSAGE = environ.get(
    'FREE_BASICS_URL_FOR_CSRF_MESSAGE', '')

AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

if AWS_STORAGE_BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

RABBITMQ_MANAGEMENT_INTERFACE = environ.get(
    'RABBITMQ_MANAGEMENT_INTERFACE')

FACEBOOK_PIXEL = '413876948808281'
FACEBOOK_PIXEL_COOKIE_KEY = 'facebook_pixel_hit_count'

MAINTENANCE_MODE_TEMPLATE = 'maintenance.html'
MAINTENANCE_MODE = environ.get('MAINTENANCE_MODE', None)

REFERRER_POLICY = "origin"
