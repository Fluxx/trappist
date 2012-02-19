from django.http import HttpResponse
from django.conf.urls.defaults import patterns, include, url


class Trappist(object):

    def __init__(self, app):
        self.app = app

    def start_response(self, status, headers):
        pass

    def __call__(self, request, mountpoint):
        request.environ['PATH_INFO'] = request.environ['PATH_INFO'].lstrip('/' + mountpoint)
        result = self.app(request.environ, self.start_response)
        return HttpResponse(result)

    def mounted_at(self, prefix):
        regex = r"^%s" % prefix
        pattern = patterns('', url(r'^', self))
        return url(regex, include(pattern), dict(mountpoint=prefix))
