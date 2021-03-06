#!/usr/bin/python

import sys
import time
import httplib
import base64
import argparse
import json
from datetime import timedelta
from pprint import pprint
import traceback


def post_service_info(args):
    body = {}

    try:
        if args['size'] is not None:
            if args['size'] == "": body['claim_size'] = None
            else: body['claim_size'] = args['size']
    
        if args['count'] is not None:
            if args['count'] == "": body['claim_count'] = None
            else: body['claim_count'] = args['count']
    
        if args['name'] is not None:
            if args['name'] == "": body['service_name'] = None
            else: body['service_name'] = args['name']
    
        if args['repo'] is not None:
            if args['repo'] == "": body['repo'] = None
            else: body['repo'] = args['repo']

        if args['commit'] is not None:
            if args['commit'] == "": body['commit_id'] = None
            else: body['commit_id'] = args['commit']

        if args['description'] is not None:
            if args['description'] == "": body['service_description'] = None
            else: body['service_description'] = args['description']
    
        service_id = args['service']
        debug = args['debug']
        username = args['key']
        password = args['secret']
        host = args['host']
        port = args['port']


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
        conn.close()

    if resp.status >= 400:
        if debug:
            raise ValueError('Response Error: %s, %s' % (resp.status, resp.reason))
#            raise ValueError('Response Error: %s, %s' % (resp.status, body))

    return json.loads(body)


if __name__ == "__main__":
    #HOST = "ec2-184-169-213-66.us-west-1.compute.amazonaws.com"
    #PORT = 50003
    DEFAULT_HOST = "restapi.pigeonmtk.twbbs.org"
    DEFAULT_PORT = 80
    
    
    parser = argparse.ArgumentParser(description='update the properties of a service')
    parser.add_argument('service', help='service identification')
    parser.add_argument('-s','--size', help='claimed size of containers')
    parser.add_argument('-c','--count', help='claimed count of containers')
    parser.add_argument('--name', help='service name')
    parser.add_argument('--repo', help='service repository')
    parser.add_argument('--commit', help='repository commit id')
    parser.add_argument('--description', help='service description')
    parser.add_argument('--key', help='developer key for authentication', required=True)
    parser.add_argument('--secret', help='developer secret for authentication', required=True)
    parser.add_argument('--host', help='API server hostname (default: restapi.pigeonmtk.twbbs.org)', default=DEFAULT_HOST)
    parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    parser.add_argument('--debug', help='print debug message', action='store_true')
    args = vars(parser.parse_args())
    
    
    resp = post_service_info(args)
    print json.dumps(resp, indent=4)
