from werkzeug.wsgi import DispatcherMiddleware
from django.http import HttpResponse
from django.conf.urls.defaults import patterns, include, url


class Trappist(object):

    def __init__(self, app):
        self.app = app

    def start_response(self, status, headers):
        pass

    def __run_and_generate_response(self, environ):
        result = self.app(environ, self.start_response)
        return HttpResponse(result)

    def __patch(self, request, mountpoint):
        patched = request.environ['PATH_INFO'].lstrip(mountpoint)
        original_script_name = request.environ.get('SCRIPT_NAME', '')
        request.environ['PATH_INFO'] = patched
        request.environ['SCRIPT_NAME'] = original_script_name + mountpoint

    def __call__(self, request, mountpoint):
        self.__patch(request, mountpoint)
        return self.__run_and_generate_response(request.environ)

    def mounted_at(self, prefix):
        regex = r"^%s" % prefix.lstrip('/')
        pattern = patterns('', url(r'^', self))
        return url(regex, include(pattern), dict(mountpoint=prefix))
