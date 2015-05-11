from . import unittest

from pypbs import util

class TestParseHost(unittest.TestCase):
    def test_parses_no_host_returns_empty_list(self):
        host = ''
        self.assertEqual(('',[]), util.parse_host(host))

    def test_parses_host_no_cpu(self):
        host = 'host.example.com'
        self.assertEqual(('host.example.com',[]), util.parse_host(host))

    def test_parses_single_cpu(self):
        host = 'host.example.com/2'
        self.assertEqual(('host.example.com',[2]), util.parse_host(host))

    def test_parses_range_single_cpu(self):
        host = 'host.example.com/0,2-4'
        self.assertEqual(('host.example.com',[0,2,3,4]), util.parse_host(host))

    def test_parses_range_multi_cpu_list(self):
        host = 'host.example.com/0,2'
        self.assertEqual(('host.example.com',[0,2]), util.parse_host(host))

class TestParseRangestring(unittest.TestCase):
    def test_parses_empty_string_returns_empty_list(self):
        self.assertEqual([], util.parse_rangestring(''))

    def test_parses_dash_range(self):
        self.assertEqual([1,2,3,4], util.parse_rangestring('1-4'))
    
    def test_parses_multi_range(self):
        self.assertEqual([1,3,5], util.parse_rangestring('1,3,5'))

    def test_parses_complex_rangestring(self):
        self.assertEqual([0,1,2,3,5,7,8,9], util.parse_rangestring('0-3,5,7-9'))
