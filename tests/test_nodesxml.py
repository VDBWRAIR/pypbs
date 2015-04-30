import xml.etree.ElementTree as ET
from . import unittest
from os.path import *

import mock
from nose.plugins.attrib import attr

from pypbs import nodesxml

NODESXML = join(dirname(__file__),'output.xml')

@attr('current')
class TestParsePbsnodesXml(unittest.TestCase):
    def setUp(self):
        tree = ET.parse(NODESXML)
        self.root = tree.getroot()
        self.nodes = nodesxml.parse_xml(self.root)

    def test_parses_comma_lists(self):
        self.assertIsInstance(
            self.nodes['host4.example.com']['jobs'], list
        )

    def test_builds_sub_dict_with_equal_signs(self):
        self.assertEqual(
            '1430334904', self.nodes['host1.example.com']['status']['rectime']
        )
        self.assertEqual(
            None, self.nodes['host1.example.com']['status']['gres']
        )

class TestParseListString(unittest.TestCase):
    def test_returns_original_string(self):
        self.assertEqual('foo', nodesxml.parse_list_string('foo'))

    def test_returns_split_list(self):
        self.assertEqual(
            ['foo','bar'], nodesxml.parse_list_string('foo,bar')
        )

    def test_returns_dictionary(self):
        self.assertEqual(
            {'foo':'bar','baz':None,'bar':'foo'},
            nodesxml.parse_list_string('foo=bar,baz=,bar=foo')
        )

    def test_parses_sub_dictionary_in_paren(self):
        self.assertEqual(
            {'foo':'bar','baz':'foo','jobs':{'1':{'foo':'1','bar':'2'},'2':{'foo':'1','bar':'2'}}},
            nodesxml.parse_list_string('foo=bar,jobs=1(foo=1,bar=2) 2(foo=1,bar=2),baz=foo')
        )
