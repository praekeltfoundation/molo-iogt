from django.conf import settings


def compress_settings(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'ENV': settings.ENV
    }


def external_link(request):
    return {
        'external_link_check': settings.EXTERNAL_LINK_CHECK,
    }
