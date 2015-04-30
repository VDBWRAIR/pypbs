#!/usr/bin/env python

import xml.etree.ElementTree as ET
from subprocess import check_output
from collections import OrderedDict

import nodesxml

def get_pbsnodes_xml():
    '''
    Return xml parsed pbsnodes -x
    '''
    xml = check_output('pbsnodes -x', shell=True)
    root = ET.fromstring(xml)
    return root

def main():
    xml = get_pbsnodes_xml()
    nodes = nodesxml.parse_xml(xml)
    import pprint
    pprint.pprint(nodes)
