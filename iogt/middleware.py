import datetime
from urlparse import urlparse

from bs4 import BeautifulSoup

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from google_analytics.utils import build_ga_params, set_cookie
from google_analytics.tasks import send_ga_tracking

from molo.core.middleware import MoloGoogleAnalyticsMiddleware


def clean_path(path):
    '''
    Converts string of URL paths to list of path elements
    '''
    if path == u'/':
        return [u'/']
    else:
        return [segment for segment
                in path.split(u'/') if segment]


def clean_paths(paths):
    '''
    Converts list of URL paths to list of
    lists containing only the strings making up the path

    sample input:
    ['/admin', '/admin/', 'profile/login/']

    sample output:
    [['admin'], ['admin'], ['profile', 'login']]
    '''
    return [clean_path(path) for path in paths]


def is_match(path, possible_matches):
    '''
    Matches segments of a URL path against a list of possible matches
    '''
    for possible_match in possible_matches:
        if possible_match == path[:len(possible_match)]:
            return True
    return False


def get_today():
    return datetime.date.today()


class SSLRedirectMiddleware(object):
    def process_request(self, request):
        https_paths = getattr(settings, 'HTTPS_PATHS', [])
        clean_https_paths = clean_paths(https_paths)
        response_should_be_secure = self.response_should_be_secure(
            request, clean_https_paths)
        request_is_secure = self.request_is_secure(request)
        if response_should_be_secure and not request_is_secure:
            return HttpResponsePermanentRedirect(
                "https://{}{}".format(request.get_host(),
                                      request.get_full_path())
            )

    def response_should_be_secure(self, request, https_paths):
        request_path = clean_path(request.path)
        return is_match(request_path, https_paths)

    def request_is_secure(self, request):
        if 'HTTP_X_FORWARDED_PROTO' in request.META:
            return request.META['HTTP_X_FORWARDED_PROTO'] == 'https'

        return False


class IogtMoloGoogleAnalyticsMiddleware(MoloGoogleAnalyticsMiddleware):
    """Uses GA IDs stored in Wagtail to track pageviews using celery"""
    def submit_tracking(self, account, request, response):
        try:
            title = BeautifulSoup(
                response.content, "html.parser"
            ).html.head.title.text.encode('utf-8')
        except Exception:
            title = None

        path = request.get_full_path()
        referer = request.META.get('HTTP_REFERER', '')
        params = build_ga_params(
            request, account, path=path, referer=referer, title=title)
        response = set_cookie(params, response)

        def calculate_age(dob):
            today = get_today()
            return (today.year - dob.year -
                    ((today.month, today.day) < (dob.month, dob.day)))

        # send user unique id and details after cookie's been set
        if hasattr(request, 'user') and hasattr(request.user, 'profile'):
            profile = request.user.profile

            custom_params = {}
            if profile.gender:
                gender_key = settings.GOOGLE_ANALYTICS_GENDER_KEY
                custom_params[gender_key] = profile.gender
            if profile.date_of_birth:
                age_key = settings.GOOGLE_ANALYTICS_AGE_KEY
                custom_params[age_key] = calculate_age(profile.date_of_birth)

            params = build_ga_params(
                request, account, path=path, referer=referer, title=title,
                custom_params=custom_params)

        send_ga_tracking.delay(params)
        return response
