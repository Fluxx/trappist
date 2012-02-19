from flask import Flask, url_for


app = Flask(__name__)


@app.route('/')
def test():
    return 'Hello from the root of a Flask app!'


@app.route('/test2/<name>')
def test2(name):
    url = url_for('test2', name=name)
    return 'Hello from the root of the sub url, %s (%s)' % (name, url)
