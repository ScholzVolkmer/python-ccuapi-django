"""Akamai CCU REST API

Usage:
    ccuapi length [--username=<username>] [--password=<password>]
    ccuapi status <progressUri> [--username=<username>] [--password=<password>]
    ccuapi purge (--cpcode=<cpcode> | --url=<url>) [--type=<type>] [--domain=<domain>] [--username=<username>] [--password=<password>]

Options:
    --type=<type>           # arl or cpcode defaults to arl
    --username=<username>   # username to authenticate
    --password=<password>   # password to authenticate
    --domain=<domain>       # production or staging defaults to 
    --cpcode=<cpcode>       # cpcode to purge
    --url=<url>           # Domainpath to purge

"""
from docopt import docopt
import json
from ccuapi import APIRequest

def __main__():
    arguments = docopt(__doc__)
    username = arguments['--username'] if arguments['--username'] else False
    password = arguments['--password'] if arguments['--password'] else False

    req = APIRequest(username=username, password=password)

    if arguments['length']:
        response = req.length()
        print json.dumps(response, indent=4, sort_keys=False)
        return

    if arguments['status']:
        progressUri = arguments['<progressUri>']
        response = req.status(progressUri)
        print json.dumps(response, indent=4, sort_keys=False)
        return

    if arguments['purge']:
        if arguments['--cpcode']:
            req.add_cpcode(arguments['--cpcode'])

        if arguments['--url']:
            req.add_url(arguments['--url'])

        if arguments['--domain']:
            req.domain = arguments['--domain']

        if arguments['--type']:
            req.domain = arguments['--type']

        response = req.purge()
        print json.dumps(response, indent=4, sort_keys=False)
        return

