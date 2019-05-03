import urllib
import re

from os import environ
from pyrabbit.api import Client
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import status


def health_iogt(request):
    status_code = status.HTTP_200_OK

    if settings.RABBITMQ_MANAGEMENT_INTERFACE:
        rx = re.compile(r"amqp://(?P<username>[^:]+).*?:(?P<password>[^@]+)."
                        "*/(?P<vhost>[^&]+)")
        match = rx.search(settings.BROKER_URL)

        username = match.groupdict()['username']
        password = match.groupdict()['password']
        vhost = match.groupdict()['vhost']
        base_url = settings.RABBITMQ_MANAGEMENT_INTERFACE

        mq_client = Client(base_url, username, password)
        queue_data = mq_client.get_queue(vhost, 'celery')

        messages = queue_data['messages']
        rate = queue_data['messages_details']['rate']

        if (messages > 0 and rate == 0):
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    app_id = environ.get('MARATHON_APP_ID', None)
    ver = environ.get('MARATHON_APP_VERSION', None)
    return JsonResponse({'id': app_id, 'version': ver}, status=status_code)


class ExternalLink(TemplateView):
    template_name = "core/external-link.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["next"] = self.request.GET.get("next")
        return context
