import re

def parse_xml(nodes_xml):
    '''
    Parse pbsnodes -x xml output

    :param xml.etree.ElementTree.Element nodes_xml: etree xml from pbsnodes -x
    :return: dict of {nodename: {attr1:val,}}
    '''
    nodes = {}
    for node in nodes_xml:
        tdict = {}
        for attrib in node:
            tdict[attrib.tag] = parse_list_string(attrib.text)
        nodes[tdict['name']] = tdict
    return nodes

def parse_list_string(string):
    '''
    Parse out any list like string that is separated by comma
    If individual list items have key=value, convert to dict
    If there are no commas then just return original string
    '''
    parts = re.split('(?<=[\w\)=]),(?=\w)',string)
    # Return original string
    if len(parts) == 1:
        return string

    # No sub dictionary required
    if '=' not in string:
        return parts

    _dict = {}
    for i in range(len(parts)):
        part = parts[i]
        # No subdict
        if '(' not in part and ')' not in part:
            k,v = part.split('=')
            if not v:
                v = None
            _dict[k] = v

    # Now do another search for subdict patterns
    subdict = {}
    p = '(\w+)=((?:\w\(\S+\)\s{0,1})+)'
    stuff = re.findall(p, string)
    for key, values in stuff:
        subdict[key] = {}
        defs = re.findall('(?:(\w)\((.*?)\))', values)
        for _key, d in defs:
            subdict[key][_key] = parse_list_string(d)
    _dict.update(subdict)
    return _dict
