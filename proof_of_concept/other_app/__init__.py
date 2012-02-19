from flask import Flask

app = Flask(__name__)

# TODO:
#   - Look at how flask generates URLs, and make sure that works when it is now
#     mounted at a subfolder

@app.route('/')
def test():
    return 'Hello from the root of a Flask app!'

@app.route('/test2')
def test2():
    return 'Hello from the root of the sub url'