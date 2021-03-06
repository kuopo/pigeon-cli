#!/usr/bin/python

import sys
import time
import httplib
import urllib2
import base64
import argparse
import json
from datetime import timedelta
from pprint import pprint
import traceback


def delete_service_info(args):
    try:
        service_list = args['service']
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

        conn.request('DELETE', "/service/" + "/".join(service_list), headers=headers)
        
        resp = conn.getresponse()
        body = resp.read()

    except Exception as e:
        if debug:
            traceback.print_exc(file=sys.stdout)
            raise Exception('Connection Error: %s' % e)
        else:
            return {"message": "Some error happens..."}
    finally:
        if conn is not None: conn.close()

#    if resp.status >= 400:
#        body = resp.read()
#	print body
#	return
#        raise ValueError('Response Error: %s, %s' % (resp.status, resp.reason))
    return json.loads(body)


if __name__ == "__main__":
    #HOST = "ec2-184-169-213-66.us-west-1.compute.amazonaws.com"
    #PORT = 50003
    HOST = "restapi.pigeonmtk.twbbs.org"
    PORT = 80
    
    
    parser = argparse.ArgumentParser(description='delete a service')
    parser.add_argument('service', nargs='+', default='', help='service identification')
    parser.add_argument('--key', help='developer key for authentication', required=True)
    parser.add_argument('--secret', help='developer secret for authentication', required=True)
    parser.add_argument('--host', help='API server hostname (default: restapi.pigeonmtk.twbbs.org)', default=HOST)
    parser.add_argument('--port', help='API server port (default: 80)', default=PORT)
    parser.add_argument('--debug', help='print debug message', action='store_true')
    args = vars(parser.parse_args())
    
    
    resp = delete_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)
