from flask import Flask
from django.http import HttpResponse
from django.conf.urls.defaults import patterns, include, url

app = Flask(__name__)

# TODO:
#   - Look at URL generation at the subfolder

@app.route('/')
def test():
    return 'Hello from the root of a Flask app!'


class Trappist(object):

    def __init__(self, app):
        self.app = app

    def start_response(self, status, headers):
        pass
        # print 'status', status
        # print 'headers', headers

    def __call__(self, request, mountpoint):
        request.environ['PATH_INFO'] = request.environ['PATH_INFO'].lstrip('/' + mountpoint)
        result = self.app(request.environ, self.start_response)
        return HttpResponse(result)

    def mounted_at(self, prefix):
        regex = r"^%s" % prefix
        pattern = patterns('', url(r'^$', 'other_app.trappist'))
        return url(regex, include(pattern), dict(mountpoint=prefix))

trappist = Trappist(app)