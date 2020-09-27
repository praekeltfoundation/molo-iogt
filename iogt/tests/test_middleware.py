import mock
import datetime
import responses

import pytest

from django.test import TestCase, Client, RequestFactory, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import escape_uri_path
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory, override_settings

from molo.core.models import (
    Languages, SiteLanguageRelation, Main, SectionIndexPage)
from molo.core.tests.base import MoloTestCaseMixin

from wagtail.wagtailsearch.backends import get_search_backend

from iogt.middleware import (
    SSLRedirectMiddleware, IogtMoloGoogleAnalyticsMiddleware, clean_path,
    clean_paths, is_match,
)


PERMANENT_REDIRECT_STATUS_CODE = 301


def override_get_today():
    return datetime.date(2017, 1, 1)


class TestMiddlewareUtils(TestCase):
    def test_clean_path(self):
        self.assertEqual(clean_path(u'/'), [u'/'])
        self.assertEqual(clean_path('/admin'), ['admin'])
        self.assertEqual(clean_path('/admin/'), ['admin'])
        self.assertEqual(clean_path('admin/'), ['admin'])
        self.assertEqual(clean_path('admin'), ['admin'])
        self.assertEqual(clean_path('admin/login'), ['admin', 'login'])
        self.assertEqual(clean_path('/admin/login/'), ['admin', 'login'])
        self.assertEqual(clean_path('admin/login/'), ['admin', 'login'])
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
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(self.main.get_site()),
            locale='en', is_active=True
        )
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


class TestGoogleAnalyticsMiddleware(TestCase, MoloTestCaseMixin):

    def setUp(self):
        # Creates Main language
        self.mk_main()
        self.main = Main.objects.all().first()
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(self.main.get_site()),
            locale='en', is_active=True,
        )
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testuser', password='password', email='test@email.com')
        profile = self.superuser.profile
        profile.gender = 'female'
        profile.date_of_birth = datetime.date(2000, 1, 1)
        profile.save()

        self.section_index = SectionIndexPage.objects.child_of(
            self.main
        ).first()
        self.english_section = self.mk_section(
            self.section_index, title='English section')

    def make_fake_request(self, url, headers={}):
        """
        We don't have any normal views, so we're creating fake
        views using django's RequestFactory
        """
        rf = RequestFactory()
        request = rf.get(url, **headers)
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session.save()
        request.user = self.superuser
        return request

    @responses.activate
    @mock.patch('iogt.middleware.get_today', override_get_today)
    @mock.patch("google_analytics.tasks.send_ga_tracking.delay")
    def test_ga_middleware(self, mock_method):
        """
        When a url is request the path that goes to GA must include the gender
        and age if available.
        """

        self.backend = get_search_backend('default')
        self.backend.reset_index()
        self.mk_articles(self.english_section, count=2)
        self.backend.refresh_index()

        response = self.client.get(reverse('search'), {
            'q': 'Test'
        })
        headers = {'HTTP_X_IORG_FBS_UIP': '100.100.200.10'}
        request = self.make_fake_request(
            '/search/?q=Test', headers)

        middleware = IogtMoloGoogleAnalyticsMiddleware()
        account = ''
        response = middleware.submit_tracking(account, request, response)

        mock_method.assert_called()

        args, kwargs = mock_method.call_args_list[0]
        url = args[0]['utm_url']

        self.assertTrue('cd1=17' in url)
        self.assertTrue('cd2=female' in url)


class TestFaceBookPixelHistoryCounter(TestCase, MoloTestCaseMixin):
    def setUp(self):
        # Creates Main language
        self.mk_main()
        self.main = Main.objects.all().first()
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(self.main.get_site()),
            locale='en', is_active=True,
        )
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testuser', password='password', email='test@email.com')
        profile = self.superuser.profile
        profile.gender = 'female'
        profile.date_of_birth = datetime.date(2000, 1, 1)
        profile.save()

        self.section_index = SectionIndexPage.objects.child_of(
            self.main
        ).first()
        self.english_section = self.mk_section(
            self.section_index, title='English section')

    @pytest.mark.skip(reason="Set up Facebook pixel tracking (or remove)")
    def test_more_that_3_page_views(self):
        """ test if the no script html tag exists """
        view_count = 5
        self.client.cookies.load(
            {settings.FACEBOOK_PIXEL_COOKIE_KEY: view_count}
        )
        response = self.client.get(reverse('search'))
        self.assertEqual(
            int(response.client.cookies.get(
                settings.FACEBOOK_PIXEL_COOKIE_KEY
            ).value),
            view_count + 1
        )

    @pytest.mark.skip(reason="Set up Facebook pixel tracking (or remove)")
    def test_less_that_3_page_views(self):
        """ test if the no script html tag exists """
        response = self.client.get(reverse('search'))
        self.assertEqual(
            int(response.client.cookies.get(
                settings.FACEBOOK_PIXEL_COOKIE_KEY
            ).value),
            1
        )


class TestReferrerPolicyMiddleware(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.main = Main.objects.all().first()
        self.english = SiteLanguageRelation.objects.create(
            language_setting=Languages.for_site(self.main.get_site()),
            locale='en', is_active=True
        )
        self.main = Main.objects.all().first()
        self.factory = RequestFactory()
        self.client = Client()

    def test_referrer_policy_middleware(self):
        response = self.client.get(reverse('search'))
        self.assertIn("Referrer-Policy", response)
        self.assertEqual(response["Referrer-Policy"], settings.REFERRER_POLICY)
