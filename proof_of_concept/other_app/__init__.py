from flask import Flask
from django.http import HttpResponse

app = Flask(__name__)

@app.route('/')
def test():
    return 'Hello from the root of a Flask app!'


class Trappist(object):

    def __init__(self, app):
        self.app = app

    def start_response(self, status, headers):
        print 'status', status
        print 'headers', headers

    def __call__(self, request):
        result = self.app(request.environ, self.start_response)
        return HttpResponse(result)


trappist = Trappist(app)