import os
from flask import Flask, abort, make_response, redirect, send_from_directory
app = Flask(__name__)


# TODO:
#   - Verify more complicated flask things work
#     - Middlewares


@app.route('/string')
def string():
    return 'Hello World!'


@app.route('/404/raise')
def raise_404():
    abort(404)


@app.route('/404/make_request')
def make_404():
    return make_response('not found', 404)


@app.route('/500/raise')
def raise_500():
    abort(500)


@app.route('/500/make_request')
def make_500():
    return make_response('not found', 500)


@app.route('/make-header/<key>/<path:value>')
def make_header(key, value):
    response = make_response()
    response.headers[key] = value
    return response


@app.route('/redirect_to_google/<int:status>')
def redirect_to_google(status):
    return redirect('http://www.google.com', status)


@app.route('/download')
def download():
    test_app_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(test_app_dir, 'ewok.jpg', as_attachment=True)
