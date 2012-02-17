Trappist
========

**Currently a work in progress.  Not ready for production yet**

Trappist is a Python library which allows you to mount your Flask application inside of your Django application.  It translates a call to a "Django view" to a call to a Flask app, and handles the translation of the Flask app response back to Django.