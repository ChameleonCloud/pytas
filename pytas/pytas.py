#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from requests.auth import HTTPBasicAuth

"""
Client class for the TAS REST APIs.
"""
class client:

    """
    Instantiate the API Object with a base URI and service account credentials.
    The credentials should be a hash with keys `username` and `password` for
    BASIC Auth.
    """
    def __init__(self, baseURL = None, credentials = None):
        if (baseURL == None):
            baseURL = os.environ.get('TAS_URL')

        if (credentials == None):
            key = os.environ.get('TAS_CLIENT_KEY')
            secret = os.environ.get('TAS_CLIENT_SECRET')
            credentials = {'username':key, 'password':secret}

        self.baseURL = baseURL
        self.auth = HTTPBasicAuth(credentials['username'], credentials['password'])

    """
    Authenticate a user
    """
    def authenticate(self, username, password):
        payload = {'username': username, 'password': password}
        r = requests.post(self.baseURL + '/auth/login', data=payload, auth=self.auth)
        return r.json()

    """
    Projects
    """
    def project(self, id):
        headers = { 'content-type':'application/json' }
        r = requests.get(self.baseURL + '/tup/projects/' + id, headers=headers, auth=self.auth)
        return r.json()

    def projectsForUser(self, username):
        headers = { 'content-type':'application/json' }
        r = requests.get(self.baseURL + '/tup/projects/username/' + username, headers=headers, auth=self.auth)
        return r.json()
