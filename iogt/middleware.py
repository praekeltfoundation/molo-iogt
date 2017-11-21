from urlparse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


def clean_path(path):
    '''
    Converts string of URL paths to list of path elements
    '''
    if path == u'/':
        return [u'/']
    else:
        return filter(lambda a: a != '', path.split('/'))


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
