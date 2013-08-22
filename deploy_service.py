#!/usr/bin/python

import sys
import time
import httplib
import base64
import argparse
import subprocess
import json
from datetime import timedelta
from pprint import pprint
import traceback


def post_service_info(args):
    body = {}
    conn = None

    try:
        service_id = args['service']
        debug = args['debug']
        username = args['key']
        password = args['secret']
        host = args['host']
        port = args['port']
        repo = args['repo']


	if repo is None:
            repo = get_repo(args)

            if repo is None:
                return {"message": "Need specify a repository"}
            else:
                body['repo'] = repo
        else:
            body['repo'] = repo

        if args['commit'] is not None:
            if args['commit'] == "": body['commit_id'] = None
            else: body['commit_id'] = args['commit']
        else:
            s = subprocess.Popen(('git ls-remote --heads %s' % repo).split(), stdout=subprocess.PIPE)
            commit = s.communicate()[0].strip().split()[0]
            body['commit_id'] = commit


        conn = httplib.HTTPConnection(host=host, port=port)
        if debug: conn.set_debuglevel(1)
        conn.connect()
        request = conn.putrequest('PUT', '/service/%s' % (service_id))
        reqbody = json.dumps(body)
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Content-Length'] = "%d" % (len(reqbody))
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        headers['Authorization'] = "Basic " + base64string
        for k in headers:
            conn.putheader(k, headers[k])
        conn.endheaders()

        conn.send(reqbody)

        resp = conn.getresponse()
        body = resp.read()

    except Exception as e:
        if debug:
            traceback.print_exc(file=sys.stdout)
            raise Exception('Connection Error: %s' % e)
        else:
            return {"message": "Some error happens..."}
    finally:
        if conn != None: conn.close()

    if resp.status >= 400:
        if debug:
            raise ValueError('Response Error: %s, %s' % (resp.status, resp.reason))
#            raise ValueError('Response Error: %s, %s' % (resp.status, body))

    return json.loads(body)


def get_repo(args):
    try:
        service_id = args['service']
        username = args['key']
        password = args['secret']
        debug = args['debug']
        host = args['host']
        port = args['port']

        conn = httplib.HTTPConnection(host=host, port=port)

        if debug: conn.set_debuglevel(1)

        headers = {}
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        headers = {'Authorization': 'Basic ' + base64string}

        conn.request('GET', "/service/%s" % service_id, headers=headers)

        resp = conn.getresponse()
        body = resp.read()
        repo = json.loads(body)[0]['repo']

#    except Exception as e:
#        if debug:
#            traceback.print_exc(file=sys.stdout)
#            raise Exception('Connection Error: %s' % e)
#        else:
#            return {"message": "Some error happens..."}
    finally:
        if conn is not None: conn.close()

    return repo


if __name__ == "__main__":
    #HOST = "ec2-184-169-213-66.us-west-1.compute.amazonaws.com"
    #PORT = 50003
    DEFAULT_HOST = "restapi.pigeonmtk.twbbs.org"
    DEFAULT_PORT = 80
    
    
    parser = argparse.ArgumentParser(description='deploy a service given a repository')
    parser.add_argument('service', help='service identification')
    parser.add_argument('--repo', help='service repository')
    parser.add_argument('--commit', help='repository commit id (fetch from the HEAD of remote repo)')
    parser.add_argument('--key', help='developer key for authentication', required=True)
    parser.add_argument('--secret', help='developer secret for authentication', required=True)
    parser.add_argument('--host', help='API server hostname (default: restapi.pigeonmtk.twbbs.org)', default=DEFAULT_HOST)
    parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    parser.add_argument('--debug', help='print debug message', action='store_true')
    args = vars(parser.parse_args())
    
    
    resp = post_service_info(args)
    print json.dumps(resp, indent=4)
