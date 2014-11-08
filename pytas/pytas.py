#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from suds.client import Client as Suds

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
        self.credentials = credentials
        self.auth = HTTPBasicAuth(credentials['username'], credentials['password'])

    """
    Authenticate a user
    """
    def authenticate(self, username, password):
        payload = {'username': username, 'password': password}
        r = requests.post(self.baseURL + '/auth/login', data=payload, auth=self.auth)
        resp = r.json()
        if resp['status'] == 'success':
            return resp['result']
        else:
            raise Exception('Authentication Error', resp['message'])

    """
    Users
    """
    def get_user(self, id = None, username = None):
        if id:
            url = '{0}/v1/users/{1}'.format(self.baseURL, id)
        elif username:
            url = '{0}/v1/users/username/{1}'.format(self.baseURL, username)
        else:
            raise Exception('username or id is required!')

        r = requests.get(url, auth=self.auth);
        resp = r.json()
        if resp['status'] == 'success':
            return resp['result']
        else:
            raise Exception('User not found', resp['message'])

    """
    Data Lists
    Institutions/Departments
    """
    def institutions(self):
        url = self.baseURL.replace('/api', '/TASWebService/PortalService.asmx?wsdl')
        api = Suds(url, username=self.credentials['username'], password=self.credentials['password'])
        resp = api.service.GetInstitutions()
        institutions = []
        for i in resp.Institution:
            if i.Validated:
                inst = {
                    'id': i.ID,
                    'name': i.Name,
                    'active': i.Selectable,
                    'children': self._get_departments(i)
                }

                institutions.append(inst)

        return institutions

    def _get_departments(self, institution):
        depts = []

        if institution.Children:
            for child in institution.Children.Institution:
                depts.append({
                    'id': child.ID,
                    'name': child.Name,
                    'active': child.Selectable,
                    'children': []
                })
                if child.Children:
                    depts.extend(self._get_departments(child))

        return depts

    def countries(self):
        url = self.baseURL.replace('/api', '/TASWebService/PortalService.asmx?wsdl')
        api = Suds(url, username=self.credentials['username'], password=self.credentials['password'])
        resp = api.service.GetCountries()
        countries = []

        for c in resp.Country:
            countries.append({
                'id': c.ID,
                'name': c.Name
            })

        return countries

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
