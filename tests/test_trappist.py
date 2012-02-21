import unittest
import mock
from nose.tools import *

from django.conf import settings
settings.configure(DEBUG=True)

from django.core.urlresolvers import RegexURLResolver
from django.test.client import RequestFactory

from trappist import Trappist


class TestTrappist(unittest.TestCase):

    def setUp(self):
        self.app = mock.Mock()
        self.trappist = Trappist(self.app)
        self.req = RequestFactory()

    def request(self, path='/mnt'):
        return self.trappist(self.req.get(path), mountpoint='/mnt')

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
        ok_(self.trappist(self.req.get('/mnt'), mountpoint='/mnt'))

    def test_patches_environment_path_info_and_script_name_to_remove_mount(self):
        self.trappist.app = mock.Mock()
        self.request('/mnt/another/path')
        args, kwargs = self.trappist.app.call_args

        eq_(args[0]['PATH_INFO'], '/another/path')
        eq_(args[0]['SCRIPT_NAME'], '/mnt')
