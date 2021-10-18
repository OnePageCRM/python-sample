#!/usr/bin/env python

from base64 import b64decode
import requests
import json

class OnePageCRMAPI():
    def __init__(self, user_id, api_key):
        '''\
        Initializes the OnePageAPI object and authenticates
        with the OnePageCRM API.
        Requires user_id and api_key of an active OnePageCRM user

        You can get a list of contacts with the get_contacts method.
        '''
        self.user_id = user_id
        self.api_key = api_key

    def get_contacts(self):
        '''\
        Returns a list of contacts in JSON format\
        '''
        url = 'https://app.onepagecrm.com/api/v3/contacts.json'

        response = requests.get(url, auth=(user_id, api_key))

        if response.json()['status'] == 0:
            return response.json()['data']['contacts']
        else:
            raise Exception(response.json()['error_message'])

user_id = 'xxxxxx' # Insert your user_id here
api_key = 'xxxxxx' # Insert your api_key here

client = OnePageCRMAPI(user_id, api_key)

contacts = client.get_contacts()
print(json.dumps(contacts, indent=4, sort_keys=True))
