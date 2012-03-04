from django.http import HttpResponse
from django.conf.urls.defaults import patterns, include, url
import re


class Trappist(object):

    STATUS_INT = re.compile('^\d+')

    def __init__(self, app):
        self.app = app

    def mounted_at(self, prefix):
        regex = r"^%s" % prefix.lstrip('/')
        pattern = patterns('', url(r'^', self))
        return url(regex, include(pattern), dict(mountpoint=prefix))

    def start_response(status, headers):
        pass

    def __call__(self, request, mountpoint):
        self.__patch(request, mountpoint)
        return self.__run_and_generate_response(request.environ)

    # TODO:
    #   - Setup project and testing
    #   - Handle non-200 errors from Flask and propgate to Django
    #   - Verify more complicated flask things work
    #     - Blueprints
    #     - Templates
    #     - Redirection
    #     - Static Files
    #     - Request data
    #     - Cookie path + cookies
    #     - Middlewares
    def __run_and_generate_response(self, environ):
        status_headers = [None, None]

        def start_response(status, headers):
            # Convert the string statu to a number
            match = self.STATUS_INT.search(status)
            status_headers[:] = [int(match.group()), headers]

        body = self.app(environ, start_response)
        status, headers = status_headers
        print headers
        # Args to handle
        # - mimetype
        # - content_type
        return HttpResponse(body, status=status)

    def __patch(self, request, mountpoint):
        patched = request.environ['PATH_INFO'][len(mountpoint):]
        original_script_name = request.environ.get('SCRIPT_NAME', '')
        request.environ['PATH_INFO'] = patched
        request.environ['SCRIPT_NAME'] = original_script_name + mountpoint
