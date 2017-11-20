from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class SSLRedirectMiddleware(object):
    def process_request(self, request):
        HTTPS_PATHS = getattr(settings, 'HTTPS_PATHS', [])
        response_should_be_secure = self.response_should_be_secure(
            request, HTTPS_PATHS)
        request_is_secure = self.request_is_secure(request)
        if response_should_be_secure and not request_is_secure:
            return HttpResponsePermanentRedirect(
                "https://{}{}".format(request.get_host(),
                                      request.get_full_path())
            )

    def response_should_be_secure(self, request, HTTPS_PATHS):
        for path in HTTPS_PATHS:
            if request.path.startswith(u'/{}'.format(path)):
                return True
        return False

    def request_is_secure(self, request):
        if 'HTTP_X_FORWARDED_PROTO' in request.META:
            return request.META['HTTP_X_FORWARDED_PROTO'] == 'https'

        return False
