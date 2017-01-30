FROM praekeltfoundation/django-bootstrap

RUN apt-get-install.sh gettext

ENV PROJECT_ROOT=/app/ \
    DJANGO_SETTINGS_MODULE=iogt.settings.docker \
    APP_MODULE="iogt.wsgi:application"

ENV CELERY_APP iogt
ENV CELERY_BEAT 1

COPY . /app

RUN pip install -e .

RUN LANGUAGE_CODE=en django-admin compilemessages && \
    django-admin compress && \
    django-admin collectstatic --noinput
