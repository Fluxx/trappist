**Note: This project is unmaintanined an no longer released on Pypi.**

Trappist
========

Trappist is a Python library which allows you to mount your Flask or other WSGI application inside of your Django application.  It translates a call to a "Django view" to a call to a WSGI, and handles the translation of the Flask app response back as a Django `HttpResponse` object.

Usage
=====

To use Trappist, simply construct a new ``Trappist`` object to wrap your existing WSGI application, and call ``mounted_at('/path')`` to mount the app at that location.  For example, here is a "blog" WSGI app mounted at '/blog' inside an existing Django application::

    from django.conf.urls.defaults import patterns, include, url
    from my_blog import app
    from trappist import Trappist

    urlpatterns = patterns('',
        Trappist(app).mounted_at('/blog'),
        (r'^articles/(?P<year>\d{4})/$', 'news.views.year_archive'),
        (r'^comments/', include('django.contrib.comments.urls'))
    )

The root of the blog application would then be accessible at ``/blog``, relative to the Django application root.

Note: The mountpoint passed to ``mounted_at`` must be a string with a leading forward slash (/).  Any other form of mountpoint prefix is not supported.
