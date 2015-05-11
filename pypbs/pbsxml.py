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
            if attrib.tag == 'jobs':
                tdict[attrib.tag] = parse_job_list(attrib.text)
            else:
                tdict[attrib.tag] = parse_list_string(attrib.text)
        if 'jobs' not in tdict:
            tdict['jobs'] = []
        elif isinstance(tdict['jobs'],str):
            tdict['jobs'] = [tdict['jobs']]
        nodes[tdict['name']] = tdict
    return nodes

def parse_list_string(string):
    '''
    Parse out any list like string that is separated by comma
    If individual list items have key=value, convert to dict
    If there are no commas then just return original string

    :param str string: list like string
    :return: list or dict depending on input string
    '''
    # Splits on comma if word or equal sign on the left and word on the right
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
    p = '(\w+)=([\w\d\.]+\(.*?\)(?: \S+\(.*?\)){0,})'
    stuff = re.findall(p, string)
    for key, values in stuff:
        subdict[key] = {}
        defs = re.findall('(?:(\S+)\((.*?)\))', values)
        for _key, d in defs:
            subdict[key][_key] = parse_list_string(d)
    _dict.update(subdict)
    return _dict

def parse_job_list(joblist):
    '''
    Parses a joblist

    :param str joblist: string of jobs
    :return: list of separated jobs
    '''
    jobs = re.split('(?<=[a-zA-Z]),(?=\d)', joblist)
    return list(filter(lambda x: x != '', jobs))
