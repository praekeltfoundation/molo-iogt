from django.test import (
    TestCase,
    Client,
    RequestFactory,
    override_settings,
)

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import Main

from iogt.middleware import (
    SSLRedirectMiddleware,
    clean_path,
    clean_paths,
    is_match,
)


PERMANENT_REDIRECT_STATUS_CODE = 301


class TestMiddlewareUtils(TestCase):
    def test_clean_path(self):
        self.assertEqual(clean_path(u'/'), [u'/'])
        self.assertEqual(clean_path('/admin'), ['admin'])
        self.assertEqual(clean_path('/admin/'), ['admin'])
        self.assertEqual(clean_path('admin/'), ['admin'])
        self.assertEqual(clean_path('admin'), ['admin'])
        self.assertEqual(clean_path('admin/login'), ['admin', 'login'])
        self.assertEqual(clean_path('/admin/login/'), ['admin', 'login'])
        self.assertEqual(clean_path('admin/login'), ['admin', 'login'])
        self.assertEqual(clean_path('/admin/login'), ['admin', 'login'])
        self.assertEqual(clean_path('/admin/login/extra'),
                         ['admin', 'login', 'extra'])

    def test_clean_paths(self):
        self.assertEqual(
            clean_paths([]), []
        )
        self.assertEqual(
            clean_paths(['/admin', '/admin/', 'admin/', 'admin']),
            [['admin'], ['admin'], ['admin'], ['admin']]
        )

    def test_is_match(self):
        self.assertTrue(
            is_match(['admin'], [['admin']])
        )
        self.assertFalse(
            is_match(['admin'], [['admin-django']])
        )
        self.assertFalse(
            is_match(['profiles'], [['profiles', 'login']])
        )
        self.assertTrue(
            is_match(['profiles', 'login'], [['profiles', 'login']])
        )
        self.assertFalse(
            is_match(['profiles', 'login'], [['profiles', 'register']])
        )
        self.assertTrue(
            is_match(['profiles', 'login'], [['admin'], ['profiles', 'login']])
        )
        self.assertFalse(
            is_match(['profiles', 'login'], [])
        )
        self.assertTrue(
            is_match(['/'], [['/']])
        )
        self.assertTrue(
            is_match(['/'], [['admin'], ['/']])
        )


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
