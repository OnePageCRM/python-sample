#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import sha256
from hashlib import sha1
from time import time
import hmac
from base64 import b64decode
import requests
try:
    import json
except ImportError:
    import simplejson as json


class OnePageCRMAPI():

    def __init__(self, username, password):
        '''\
        Initializes the OnePageAPI object and authenticates
        with the OnePageCRM API.
        Requires username and password of an active OnePageCRM customer

        You can get a list of contacts with the get_contacts method.
        '''

        self.username = username
        self.password = password

        response = requests.post('https://app.onepagecrm.com/api/v3/login.json',
                                params={'login': self.username,
                                        'password': self.password})
        data = response.json()['data']
        self.api_key = data['auth_key']
        self.user_id = data['user_id']


    def get_contacts(self):
        '''\
        Returns a list of contacts in JSON format\
        '''

        url = 'https://app.onepagecrm.com/api/v3/contacts.json'
        payload = ''
        headers = self.construct_headers('GET', url, payload)
        response = requests.get(url, data=json.dumps(payload), headers=headers)

        return response.json()['data']['contacts']


    def construct_headers(self, method, url, request_body):
        '''\
        Compile necessary headers for communicating with OnePageCRM\
        '''

        timestamp = time()
        signature = self.onepagecrm_signature(timestamp, method, url, request_body)
        return {'X-OnePageCRM-UID': self.user_id,
                'X-OnePageCRM-TS': '%0.f' % (timestamp),
                'X-OnePageCRM-Auth': str(signature),
                'Content-Type': 'application/json',
                'accept': 'application/json'}

    def onepagecrm_signature(self, timestamp, request_type, request_url, request_body = ''):
        '''\
        Creates the signature needed for the Headers\
        '''

        decoded_api_key = b64decode(self.api_key)

        request_url_hash = sha1(request_url.encode('utf-8')).hexdigest()

        request_body_hash = sha1(request_body.encode('utf-8')).hexdigest()

        signature_message = "%s.%0.f.%s.%s" % (self.user_id, timestamp,
          request_type.upper(), request_url_hash)

        signature_message += ('.' + request_body_hash) if request_body != '' else ''

        return hmac.new(decoded_api_key,signature_message.encode('utf-8'),sha256).hexdigest()



username = 'xxxxxxxx' # Insert your username here
password = 'xxxxxxxx' # Insert your password here

sample = OnePageCRMAPI(username, password)

contacts = sample.get_contacts()
print contacts
