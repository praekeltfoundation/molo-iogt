from django.conf import settings


def env(request):
    return {'ENV': settings.ENV}
