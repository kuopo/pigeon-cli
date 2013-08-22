#!/usr/bin/python

import argparse
import json
import create_service
import query_service
import update_service
import delete_service
import deploy_service


def create(args):
    resp = create_service.post_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)

def retrieve(args):
    resp = query_service.get_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)

def update(args):
    resp = update_service.post_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)

def delete(args):
    resp = delete_service.delete_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)

def deploy(args):
    resp = deploy_service.post_service_info(args)
    print json.dumps(resp, indent=4, sort_keys=True)


if __name__ == "__main__":
    DEFAULT_HOST = "api.pigeonaws.tk"
    DEFAULT_PORT = 80
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='valid commands')

    create_cmd_parser = subparsers.add_parser('create', description='create a hostedon service')
    create_cmd_parser.add_argument('-s','--size', help='claimed size of containers')
    create_cmd_parser.add_argument('-c','--count', help='claimed count of containers')
    create_cmd_parser.add_argument('--id', help='service ID', required=True)
    create_cmd_parser.add_argument('--name', help='service name')
    create_cmd_parser.add_argument('--repo', help='service repository')
    create_cmd_parser.add_argument('--commit', help='repository commit id')
    create_cmd_parser.add_argument('--description', help='service description')
    create_cmd_parser.add_argument('--key', help='developer key for authentication', required=True)
    create_cmd_parser.add_argument('--secret', help='developer secret for authentication', required=True)
    create_cmd_parser.add_argument('--host', help='API server hostname (default: api.pigeonaws.tk)', default=DEFAULT_HOST)
    create_cmd_parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    create_cmd_parser.add_argument('--debug', help='print debug message', action='store_true')
    create_cmd_parser.set_defaults(func=create)

    retrieve_parser = subparsers.add_parser('query', description='retrieve the properties of a service')
    retrieve_parser.add_argument('service', nargs='*', default='', help='service identification')
    retrieve_parser.add_argument('--key', help='developer key for authentication', required=True)
    retrieve_parser.add_argument('--secret', help='developer secret for authentication', required=True)
    retrieve_parser.add_argument('--host', help='API server hostname (default: api.pigeonaws.tk)', default=DEFAULT_HOST)
    retrieve_parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    retrieve_parser.add_argument('--debug', help='print debug message', action='store_true')
    retrieve_parser.set_defaults(func=retrieve)

    update_parser = subparsers.add_parser('update', description='update the properties of a service')
    update_parser.add_argument('service', help='service identification')
    update_parser.add_argument('-s','--size', help='claimed size of containers')
    update_parser.add_argument('-c','--count', help='claimed count of containers')
    update_parser.add_argument('--name', help='service name')
    update_parser.add_argument('--repo', help='service repository')
    update_parser.add_argument('--commit', help='repository commit id')
    update_parser.add_argument('--description', help='service description')
    update_parser.add_argument('--key', help='developer key for authentication', required=True)
    update_parser.add_argument('--secret', help='developer secret for authentication', required=True)
    update_parser.add_argument('--host', help='API server hostname (default: api.pigeonaws.tk)', default=DEFAULT_HOST)
    update_parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    update_parser.add_argument('--debug', help='print debug message', action='store_true')
    update_parser.set_defaults(func=update)

    delete_parser = subparsers.add_parser('delete', description='delete a service')
    delete_parser.add_argument('service', nargs='+', default='', help='service identification')
    delete_parser.add_argument('--key', help='developer key for authentication', required=True)
    delete_parser.add_argument('--secret', help='developer secret for authentication', required=True)
    delete_parser.add_argument('--host', help='API server hostname (default: api.pigeonaws.tk)', default=DEFAULT_HOST)
    delete_parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    delete_parser.add_argument('--debug', help='print debug message', action='store_true')
    delete_parser.set_defaults(func=delete)

    deploy_parser = subparsers.add_parser('deploy', description='deploy a service given a repository')
    deploy_parser.add_argument('service', help='service identification')
    deploy_parser.add_argument('--repo', help='service repository')
    deploy_parser.add_argument('--commit', help='repository commit id (fetch from the HEAD of remote repo)')
    deploy_parser.add_argument('--key', help='developer key for authentication', required=True)
    deploy_parser.add_argument('--secret', help='developer secret for authentication', required=True)
    deploy_parser.add_argument('--host', help='API server hostname (default: api.pigeonaws.tk)', default=DEFAULT_HOST)
    deploy_parser.add_argument('--port', help='API server port (default: 80)', default=DEFAULT_PORT)
    deploy_parser.add_argument('--debug', help='print debug message', action='store_true')
    deploy_parser.set_defaults(func=deploy)

    #args = vars(parser.parse_args())
    args = parser.parse_args()
    args.func(vars(args))
