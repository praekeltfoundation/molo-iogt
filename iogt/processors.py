from django.conf import settings


def env(request):
    return {'ENV': 'dev' if settings.DEBUG else 'prd'}
