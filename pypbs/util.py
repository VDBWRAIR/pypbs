import re

import sh
import xml.etree.ElementTree as ET

def parse_host(hoststring):
    '''
    Parse any host type line such as exec_host, submit_host
    
    Returns a tuple of (hostname,[cpulist])

    :param str hoststring: host string to parse
    :return: tuple(hostname,cpus)
    '''
    hostcpu = hoststring.split('/')
    if len(hostcpu) == 1:
        return (hoststring,[])
    return (hostcpu[0], parse_rangestring(hostcpu[1]))

def parse_rangestring(rangestring):
    '''
    Parses a string that represents a range of numbers
    such as 1-4 or 1 or 1,3 or combinations such as
    1-3,5,7,8-10

    :param str rangestring: range string to parse
    :returns: list of all numbers in range
    '''
    if not rangestring:
        return []
    _range = []
    parts = rangestring.split(',')
    for part in parts:
        if '-' in part:
            s,e = part.split('-')
            for i in range(int(s),int(e)+1):
                _range.append(i)
        else:
            _range.append(int(part))
    return _range

def pbs_xml_command(command, *args, **kwargs):
    '''
    Wrapper on pbs commands that can do -x to return xml output
    
    :param str command: any command but best for pbsnodes and qstat or others
                        that can do -x to return xml output
    :return: xml.etree.ElementTree
    '''
    # Ensure x flag
    kwargs['x'] = True
    xmlstr = pbs_command(command, *args, **kwargs)
    return ET.fromstring(str(xmlstr))

def pbs_command(command, *args, **kwargs):
    '''
    Simple wrapper to run pbs commands

    args and kwargs are passed on to sh.command

    :param str command: any command to run
    :return: output from command
    '''
    cmd = getattr(sh, command)
    return cmd(*args, **kwargs)
