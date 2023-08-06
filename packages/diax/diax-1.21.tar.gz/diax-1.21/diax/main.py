import argparse
import logging
import pprint

import diax.client
import diax.errors
import diax.scripting
import diax.services

LOGGER = logging.getLogger(__name__)
def _create(client, service, args):
    payload = _payload_from_args(args)
    LOGGER.info("Creating new %s resource in service %s with parameters %s", args.service, args.resource, pprint.pformat(payload))
    try:
        response = service[args.resource].post(payload)
        LOGGER.info("Created %s %s", args.resource, response)
        return 0
    except diax.errors.ValidationError as e:
        LOGGER.error("Can't create %s: %s", args.resource, e)
        return 1

def _delete(client, service, args):
    LOGGER.info("Deleting %s", args.resource)
    results = client.rawdelete(args.resource)
    LOGGER.info("Done")

def _list(client, service, args):
    LOGGER.info("Listing %s resources from %s", args.resource, args.service)
    results = service[args.resource].list()
    LOGGER.info("Results: %s", pprint.pformat(results))

def _payload_from_args(args):
    payload = {}
    for arg in args.payload:
        if '=' not in arg:
            raise Exception("You supplied the value '{arg}'. Did you mean '{arg}=something'?".format(arg=arg))
        k, _, v = arg.partition('=')
        payload[k] = v
        if payload[k] == 'true':
            payload[k] = True
        if payload[k] == 'false':
            payload[k] = False
        if payload[k] == 'null':
            payload[k] = None
    return payload

def _update(client, service, args):
    payload = _payload_from_args(args)
    LOGGER.info("Updating %s with payload %s", args.resource, pprint.pformat(payload))
    results = client.rawput(args.resource, payload)
    LOGGER.info("Done")

def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = diax.scripting.parser()
    subparsers = parser.add_subparsers(help='The command to perform')
    subparsers.required = True
    subparsers.dest = 'command'

    parser_create = subparsers.add_parser('create', help="Create a new resource")
    parser_create.set_defaults(command=_create)
    parser_create.add_argument('service',
        choices=['data', 'erp', 'quickslice', 'tetra', 'woodhouse', 'users'],
        help="The name of the service to interact with",
    )
    parser_create.add_argument('resource',
        help="The path of the resource to create such as '/model/'",
    )
    parser_create.add_argument(
        'payload',
        nargs=argparse.REMAINDER,
        help="The values to send in creating the resource with the form foo=bar",
    )

    parser_list = subparsers.add_parser('list', help="List all available resources of the given type")
    parser_list.set_defaults(command=_list)
    parser_list.add_argument('service',
        choices=['data', 'erp', 'quickslice', 'tetra', 'woodhouse', 'users'],
        help="The name of the service to interact with",
    )
    parser_list.add_argument('resource',
        help="The path of the resource to list such as '/model/'",
    )

    parser_delete = subparsers.add_parser('delete', help='Delete something')
    parser_delete.add_argument('resource', help='The URI of the resource to be deleted')
    parser_delete.set_defaults(command=_delete)

    parser_update = subparsers.add_parser('update', help='Update a resource')
    parser_update.set_defaults(command=_update)
    parser_update.add_argument('resource', help='The URI of the resource to be updated')
    parser_update.add_argument(
        'payload',
        nargs=argparse.REMAINDER,
        help="The values to send in updating the resource with the form foo=bar",
    )
    args = parser.parse_args()

    client = diax.client.create(args)
    client.login()

    if hasattr(args, 'service'):
        service = diax.services.connect(client, args.service)
    else:
        service = None


    return args.command(client, service, args)
