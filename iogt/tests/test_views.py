from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from molo.core.tests.base import MoloTestCaseMixin
from molo.commenting.models import MoloComment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site


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
