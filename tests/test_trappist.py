import unittest
import mock
from nose.tools import *

from django.conf import settings
settings.configure(DEBUG=True)

from django.core.urlresolvers import RegexURLResolver
from django.test.client import RequestFactory
import django.http

from trappist import Trappist


class TestTrappist(unittest.TestCase):

    def setUp(self):
        self.app = mock.Mock()
        self.trappist = Trappist(self.app)
        self.req_factory = RequestFactory()

    def call(self, request=None, path=None):
        req = request or self.request(path)
        return self.trappist(req, mountpoint='/mnt')

    def request(self, path='/mnt'):
        return self.req_factory.get(path)

    @property
    def mounted_at(self):
        return self.trappist.mounted_at('/mnt')

    def test_init_takes_app(self):
        trappist = Trappist(self.app)
        eq_(trappist.app, self.app)

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

    def test_created_resolver_with_self_as_callback(self):
        eq_(len(self.mounted_at.urlconf_name), 1)
        eq_(self.mounted_at.urlconf_name[0].callback, self.trappist)

    def test_call_takes_request_and_mountpoint_as_argument(self):
        ok_(self.trappist(self.req_factory.get('/mnt'), mountpoint='/mnt'))

    def test_patches_environment_path_info_and_script_name_to_remove_mount(self):
        self.trappist.app = mock.Mock()
        self.call(path='/mnt/another/path')
        args, kwargs = self.trappist.app.call_args

        eq_(args[0]['PATH_INFO'], '/another/path')
        eq_(args[0]['SCRIPT_NAME'], '/mnt')

    def test_calls_with_patched_environment_and_start_response_callable(self):
        self.trappist.app = mock.Mock()
        request = self.request('/mnt/another/path')
        self.call(request)
        self.trappist.app.assert_called_once_with(request.environ, self.trappist.start_response)

    def test_call_returns_response_wrapped_in_a_django_http_response(self):
        assert_is_instance(self.call(path='/'), django.http.HttpResponse)
