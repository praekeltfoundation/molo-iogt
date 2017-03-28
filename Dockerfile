FROM praekeltfoundation/molo-bootstrap:4.4.7-onbuild

ENV DJANGO_SETTINGS_MODULE=iogt.settings.docker \
    CELERY_APP=iogt \
    CELERY_WORKER=1 \
    CELERY_BEAT=1

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    django-admin collectstatic --noinput && \
    django-admin compress

CMD ["iogt.wsgi:application", "--timeout", "1800"]
