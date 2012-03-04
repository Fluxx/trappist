from flask import Flask, abort, make_response
app = Flask(__name__)


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
    response = make_response('not found', 500)
    response.headers[key] = value
    return response
