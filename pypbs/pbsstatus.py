#!/usr/bin/env python

import xml.etree.ElementTree as ET
import re

import sh

from . import nodesxml

def get_pbsnodes_xml(nodes=[]):
    '''
    Return xml parsed pbsnodes -x

    :param list nodes: list of nodes to retrieve info for 
    '''
    cmd = '-x'
    if nodes:
        cmd += ' ' + ' '.join(nodes)
    xml = sh.pbsnodes(cmd)
    root = ET.fromstring(str(xml))
    return root

def cluster_info(nodes_info):
    '''
    Get cluster status dictionary for all nodes
    in nodes_info.
    nodes_info needs to be information from nodesxml.parse_xml
    Cluster status will return the status of the cluster as a dictionary
    with the following keys:

        * np_utilization - used np / total np as a (float <= 1)
        * load_utilization - load ave / total ncpus (float)
        * total_np - total of all np in cluster
        * used_np - total all np used from jobs
        * avail_np - total - used
        * running_jobs - number of jobs running

    :param dict nodes_info: nodesxml.parse_xml output for nodes
    :return: dict of cluster utilization values
    '''
    cluster_info = {
        'np_utilization': 0.0,
        'load_utilization': 0.0,
        'total_np': 0,
        'used_np': 0,
        'avail_np': 0,
        'running_jobs': 0
    }
    ncpus = 0
    for nodename, nodeinfo in nodes_info.items():
        jobs = nodeinfo['jobs']
        np = int(nodeinfo['np'])
        ncpus += int(nodeinfo['status']['ncpus'])
        loadave = float(nodeinfo['status']['loadave'])
        cluster_info['total_np'] += np
        cluster_info['load_utilization'] += loadave
        for job in nodeinfo['jobs']:
            _job = parse_job_string(job)
            cluster_info['running_jobs'] += 1
            cluster_info['used_np'] += _job['ncpus']
    cluster_info['avail_np'] = cluster_info['total_np'] - cluster_info['used_np']
    cluster_info['np_utilization'] = \
        float(cluster_info['used_np']) / cluster_info['total_np']
    cluster_info['load_utilization'] = \
        cluster_info['load_utilization'] / ncpus
    return cluster_info

def parse_job_string(job_str):
    '''
    Parse a job string of cpu/jobid.submithost or
    cpu-cpu/jobid.submithost

    Returns dictionary with keys:
    
        * ncpus - number cpus used
        * cpus - actual cpu numbers used
        * jobid - id of job
        * submit_host - submit host for job
    
    :param str job_str: job string with cpusused/jobid.submithost
    :return: 
    '''
    job = {
        'ncpus': 0,
        'cpus': [],
        'jobid': 0,
        'submit_host': ''
    }
    cpus, _job = job_str.split('/')
    jobid, submithost = _job.split('.', 1)
    job['jobid'] = int(jobid)
    job['submit_host'] = submithost

    cpus = cpus.split(',')
    for cpu in cpus:
        if '-' in cpu:
            s,e = cpu.split('-')
            for i in range(int(s),int(e)+1):
                job['cpus'].append(i)
        else:
            job['cpus'].append(int(cpu))
    job['ncpus'] = len(job['cpus'])

    return job

def main():
    xml = get_pbsnodes_xml()
    nodes = nodesxml.parse_xml(xml)
    import pprint
    pprint.pprint(nodes)
