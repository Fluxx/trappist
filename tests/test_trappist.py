import unittest
import mock
from django.core.urlresolvers import RegexURLResolver
from nose.tools import *

from trappist import Trappist


class TestTrappist(unittest.TestCase):

    def setUp(self):
        self.app = mock.Mock()
        self.trappist = Trappist(self.app)

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

    def test_mounted_at_constructs_resolver_with_self_for_any_url(self):
        pass

    def test_monted_at_added_mounted_at_kw_arg_with_passed_prefix():
        pass
