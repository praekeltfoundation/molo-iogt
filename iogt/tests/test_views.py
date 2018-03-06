import requests
import json

from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from molo.core.tests.base import MoloTestCaseMixin
from molo.commenting.models import MoloComment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from mock import Mock, patch
from rest_framework import status


class ViewsTestCase(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')
        self.content_type = ContentType.objects.get_for_model(self.user)
        self.client = Client()

    def mk_comment(self, comment):
        return MoloComment.objects.create(
            content_type=self.content_type,
            object_pk=self.user.pk,
            content_object=self.user,
            site=Site.objects.get_current(),
            user=self.user,
            comment=comment,
            submit_date=datetime.now())

    def test_reporting_comment(self):
        comment = self.mk_comment('the comment')

        response = self.client.get(reverse(
            'molo.commenting:molo-comments-report', args=(comment.pk,)))

        self.assertEqual(
            response['location'],
            '/profiles/login/?next=/commenting/molo/report/1/')

        self.client.login(username='test', password='test')

        response = self.client.get(reverse(
            'molo.commenting:molo-comments-report', args=(comment.pk,)))
        self.assertEqual(response['location'], '/cr/4/1/#c1')

    @override_settings(RABBITMQ_MANAGEMENT_INTERFACE=None)
    def test_health_no_interface_set(self):
        """
        When there is no management interface configured it should not try and
        get the status of the queues
        """

        response = self.client.get(reverse('health_iogt'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_good(self):
        """
        If there is a management interface configured it should check the
        queues, if there are messages and the rate is above 0 the status should
        be OK.
        """

        details = json.dumps(
            {'messages': 1243, 'messages_details': {'rate': 1.2}})

        with patch('httplib2.Http.request') as req:
            resp = requests.Response()
            resp.status = status.HTTP_200_OK
            req.return_value = resp, details.encode()
            response = self.client.get(reverse('health_iogt'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_stuck(self):
        """
        If there is a management interface configured it should check the
        queues, if there are messages and the rate is 0 the status should be
        500.
        """

        details = json.dumps(
            {'messages': 2562, 'messages_details': {'rate': 0.0}})

        with patch('httplib2.Http.request') as req:
            resp = requests.Response()
            resp.status = status.HTTP_200_OK
            req.return_value = resp, details.encode()
            response = self.client.get(reverse('health_iogt'))

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
