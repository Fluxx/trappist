import unittest
import mock
from nose.tools import *

from django.conf import settings
settings.configure(DEBUG=True)

from django.core.urlresolvers import RegexURLResolver
from django.test.client import RequestFactory
import django.http

from trappist import Trappist
from test_app import app


class fixture(object):
    """
    Works like the built in @property decorator, except that it caches the
    return value for each instance.  This allows you to lazy-load the fixture
    only if your test needs it, rather than having it setup before *every* test
    when put in the setUp() method or returning a fresh run of the decorated
    method, which 99% of the time isn't what you want.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = self.func(*args)
            return self.cache[args]

    def __get__(self, instance, klass):
        return self.__call__(instance)


class TestTrappist(unittest.TestCase):

    def setUp(self):
        self.trappist = Trappist(self.mock_app)
        self.req_factory = RequestFactory()

    def call(self, request=None, path=None):
        req = request or self.request(path)
        return self.trappist(req, mountpoint='/mnt')

    def request(self, path='/mnt'):
        return self.req_factory.get(path)

    def mock_app_called(self, environ, start_response):
        start_response('200 OK', {})
        return ['hello world']

    @fixture
    def mock_app(self):
        return mock.Mock(side_effect=self.mock_app_called)

    @fixture
    def mounted_at(self):
        return self.trappist.mounted_at('/mnt')

    def test_init_takes_app(self):
        trappist = Trappist(self.mock_app)
        eq_(trappist.app, self.mock_app)

    def test_mounted_at_returns_django_regex_url_resolver(self):
        assert_is_instance(self.mounted_at, RegexURLResolver)

    def test_mounted_at_uses_regex_without_leading_slash(self):
        ok_(self.mounted_at.regex, r'mnt')

    def test_mounted_at_creates_resolver_at_mount_without_leading_slash(self):
        eq_(self.mounted_at.regex.pattern, '^mnt')

    def test_mounted_at_resolver_works_for_any_url(self):
        eq_(len(self.mounted_at.urlconf_name), 1)
        eq_(self.mounted_at.urlconf_name[0].regex.pattern, '^')

    def test_monted_at_added_mounted_at_kw_arg_with_passed_prefix(self):
        eq_(self.mounted_at.default_kwargs, dict(mountpoint='/mnt'))

    def test_mounted_at_sets_application_root_to_mountpoint(self):
        trappist = Trappist(app)
        trappist.mounted_at('/mnt')
        eq_(trappist.app.config['APPLICATION_ROOT'], '/mnt')

    def test_created_resolver_with_self_as_callback(self):
        eq_(len(self.mounted_at.urlconf_name), 1)
        eq_(self.mounted_at.urlconf_name[0].callback, self.trappist)

    def test_call_takes_request_and_mountpoint_as_argument(self):
        ok_(self.trappist(self.req_factory.get('/mnt'), mountpoint='/mnt'))

    def test_patches_environment_path_info_and_script_name_to_remove_mount(self):
        self.call(path='/mnt/another/path')
        args, kwargs = self.trappist.app.call_args

        eq_(args[0]['PATH_INFO'], '/another/path')
        eq_(args[0]['SCRIPT_NAME'], '/mnt')

    def test_calls_with_patched_environment(self):
        request = self.request('/mnt/another/path')
        self.call(request)
        called_environ = self.trappist.app.call_args[0][0]
        eq_(called_environ['PATH_INFO'], '/another/path')
        eq_(called_environ['SCRIPT_NAME'], '/mnt')

    def test_call_returns_response_wrapped_in_a_django_http_response(self):
        assert_is_instance(self.call(path='/'), django.http.HttpResponse)

    def test_call_returns_django_not_found_when_flask_returns_404(self):
        self.trappist = Trappist(app)
        response = self.call(path='/mnt/404/raise')
        eq_(response.status_code, 404)

    def test_call_raises_500_error_when_flask_returns_500(self):
        self.trappist = Trappist(app)
        response = self.call(path='/mnt/500/raise')
        eq_(response.status_code, 500)

    def test_passes_content_type_to_http_response(self):
        self.trappist = Trappist(app)
        response = self.call(path='/mnt/make-header/Content-Type/text/xml')
        eq_(response['Content-type'], 'text/xml')

    def test_propogates_redirects_to_django(self):
        self.trappist = Trappist(app)
        response = self.call(path='/mnt/redirect_to_google/301')
        eq_(response['Location'], 'http://www.google.com')
        eq_(response.status_code, 301)

    def test_sends_static_files(self):
        self.trappist = Trappist(app)
        response = self.call(path='/mnt/download')
        eq_(response['Content-Disposition'], 'attachment; filename=ewok.jpg')
        eq_(response['Content-Length'], '66328')
        eq_(len(response.content), 66328)
