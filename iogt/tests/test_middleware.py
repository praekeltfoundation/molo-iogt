from django.test import (
    TestCase,
    Client,
    RequestFactory,
    override_settings,
)

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import Main

from iogt.middleware import SSLRedirectMiddleware


PERMANENT_REDIRECT_STATUS_CODE = 301


@override_settings(HTTPS_PATHS=['admin'])
class TestSSLRedirectMiddleware(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.main = Main.objects.all().first()
        self.factory = RequestFactory()

    def test_no_redirect_for_home_page(self):
        request = self.factory.get('/')

        middleware = SSLRedirectMiddleware()
        response = middleware.process_request(request)

        self.assertEqual(response, None)

    def test_no_redirect_with_https(self):
        headers = {'HTTP_X_FORWARDED_PROTO': 'https'}
        request = self.factory.get('/', **headers)

        middleware = SSLRedirectMiddleware()
        response = middleware.process_request(request)

        self.assertEqual(response, None)

    def test_no_redirect_when_secure(self):
        headers = {'HTTP_X_FORWARDED_PROTO': 'https'}
        request = self.factory.get('/admin/', **headers)

        middleware = SSLRedirectMiddleware()
        response = middleware.process_request(request)

        self.assertEqual(response, None)

    def test_redirect_when_not_secure(self):
        request = self.factory.get('/admin/')

        middleware = SSLRedirectMiddleware()
        response = middleware.process_request(request)

        self.assertEqual(response.status_code,
                         PERMANENT_REDIRECT_STATUS_CODE)
