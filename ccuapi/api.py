import json
import os
import requests
import logging
import warnings
from ccuapi import AKAMAI_USERNAME, AKAMAI_PASSWORD, AKAMAI_NOTIFY_EMAIL
CCU_API_URL = 'https://api.ccu.akamai.com'

"""
PURGE_TYPES = (
    ('arl', 'ARL'),
    ('cpcode', 'CPCODE')
)

PURGE_ACTIONS = (
    ('remove', 'Remove',),
    ('invalidate', 'Invalidate',),
)

PURGE_DOMAINS = (
    ('production', 'Production',),
    ('staging', 'Production',),
)
"""

class CCUAPIException(Exception):
    pass


class APIRequest(object):
    """ Class to generate and send Requests to Akamais Content Control Utility API.
    """
    def __init__(self, username=False, password=False):
        self.username = username if username else AKAMAI_USERNAME 
        self.password = password if password else AKAMAI_PASSWORD
        self.type = 'arl'
        self.domain = 'production'
        self.action = 'remove'
        self.objects = []

        if not self.username or not self.password:
            raise CCUAPIException("No username or password set")


    def add_cpcode(self, cpcode):
        self.type = 'cpcode'
        if not cpcode in self.objects:
            self.objects.append(cpcode)

    def add_url(self, url):
        self.type = 'arl'
        if not url in self.objects:
            self.objects.append(url)

    def status(self, progressUri):
        """ Request Status of given Request

        If successfull returns JSON Object like this:
        {
           "httpStatus" : 200,
           "purgeId" : "95b5a092-043f-4af0-843f-aaf0043faaf0",
           "requestStatus" : "In-Progress"
           "submittedBy" : "test1",
           "submissionTime" : "2011-11-14T16:01:24Z",
           "completionTime" : null,
           "progressUri" : "/ccu/v2/purges/95b5a092-043f-4af0-843f-aaf0043faaf0",
           "pingAfterSeconds" : 60,
           "supportId" : "17SY1321286536069778-203514976",
        }
        """
        response = requests.get(CCU_API_URL + progressUri, auth=(self.username, self.password))
        if response.status_code == 200:
            content = json.loads(response.content)
            return content
        raise CCUAPIException("%s: %s" % (response.status_code, response.reason))

    def length(self):
        """ Requests the approximate number of purge requests in queue.
        
        If successfull returns JSON Object like this:
        {
            "httpStatus" : 200,
            "queueLength" : 17,
            "detail" : "The queue may take a minute to reflect new or removed requests.",
            "supportId" : "17QY1321286863376510-220300384",
        }
        """
        response = requests.get(CCU_API_URL + '/ccu/v2/queues/default', auth=(self.username, self.password))
        if response.status_code == 200:
            content = json.loads(response.content)
            return content
        raise CCUAPIException("%s: %s" % (response.status_code, response.reason))

    def purge(self, objects=[], purgetype=False, domain=False, action=False):
        """ Send the Purge Request for arls/urls or cpcodes in self.data['objects'].

        If successfull returns JSON Object like this:
        {
           "httpStatus" : 201,
           "detail" : "Request accepted.",
           "estimatedSeconds" : 420,
           "purgeId" : "95b5a092-043f-4af0-843f-aaf0043faaf0",
           "progressUri" : "/ccu/v2/purges/95b5a092-043f-4af0-843f-aaf0043faaf0",
           "pingAfterSeconds" : 420,
           "supportId" : "17PY1321286429616716-211907680",
        }
        """

        data = {
            "type": purgetype if purgetype else self.type,
            "domain": domain if domain else self.domain,
            "action": action if action else self.action,
            "objects": objects if objects else self.objects
        }
        response = requests.post(
            CCU_API_URL + '/ccu/v2/queues/default',
            data=json.dumps(data),
            auth=(self.username, self.password),
            headers={'Content-type': 'application/json'})

        if response.status_code == 201:
            content = json.loads(response.content)
            return content

        raise CCUAPIException("%s: %s" % (response.status_code, response.reason))
