#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
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

    def save_user(self, id, user):
        if id:
            url = '{0}/v1/users/{1}'.format( self.baseURL, id )
            method = 'PUT'
        else:
            url = '{0}/v1/users'.format( self.baseURL )
            method = 'POST'

        r = requests.request( method, url, data=user, auth=self.auth )
        resp = r.json()
        if resp['status'] == 'success':
            return resp['result']
        else:
            if id:
                raise Exception( 'Unable to save user id={0}'.format( id ), resp['message'] )
            else:
                raise Exception('Unable to save new user', resp['message'])

    def verify_user(self, id, code):
        url = '{0}/v1/users/{1}/{2}'.format( self.baseURL, id, code )
        r = requests.put( url, auth=self.auth )
        resp = r.json()
        if resp['status'] == 'success':
            return True
        else:
            raise Exception( 'Error verifying user id={0}'.format( id ), resp['message'] )

    def request_password_reset( self, username ):
        url = '{0}/v1/users/{1}/passwordResets'.format( self.baseURL, username )
        r = requests.post( url, data='', auth=self.auth )
        resp = r.json()
        print resp
        return True

    def confirm_password_reset( self, username, code, new_password ):
        url = '{0}/v1/users/{1}/passwordResets/{2}'.format( self.baseURL, username, code )
        body = {
            'password': new_password
        }
        r = requests.post( url, data=body, auth=self.auth )
        resp = r.json()
        print resp
        return True

    """
    Data Lists
    Institutions/Departments
    """
    def institutions(self):
        url = re.sub(r'/api[\-a-z]*$', '/TASWebService/PortalService.asmx?wsdl', self.baseURL)
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
        url = re.sub(r'/api[\-a-z]*$', '/TASWebService/PortalService.asmx?wsdl', self.baseURL)
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
    Fields
    """
    def fields( self ):
        r = requests.get( '{0}/tup/projects/fields'.format(self.baseURL), auth=self.auth )
        resp = r.json()
        return resp[ 'result' ]

    """
    Projects
    """
    def project( self, id ):
        headers = { 'content-type':'application/json' }
        r = requests.get( '{0}/tup/projects/{1}'.format(self.baseURL, id), headers=headers, auth=self.auth )
        resp = r.json()
        return resp['result']

    def project_allocations( self, id ):
        headers = { 'content-type':'application/json' }
        r = requests.get( '{0}/tup/projects/{1}/allocations'.format(self.baseURL, id), headers=headers, auth=self.auth )
        resp = r.json()
        return resp['result']

    def projects_for_user( self, username ):
        headers = { 'content-type':'application/json' }
        r = requests.get( '{0}/tup/projects/username/{1}'.format(self.baseURL, username), headers=headers, auth=self.auth )
        resp = r.json()
        return resp['result']

    def create_project( self, project_code, project_type, field_of_science, project_title, project_abstract, pi_user_id ):
        url = re.sub( r'/api[\-a-z]*$', '/TASWebService/PortalService.asmx?wsdl', self.baseURL )
        api = Suds( url, username=self.credentials['username'], password=self.credentials['password'] )
        project_id = api.service.CreateProject( project_code, project_type, field_of_science, 0, project_abstract, project_title, pi_user_id )
        return project_id

    def edit_project( self, project_id, project_code, field_of_science, project_title, project_abstract ):
        url = re.sub( r'/api[\-a-z]*$', '/TASWebService/PortalService.asmx?wsdl', self.baseURL )
        api = Suds( url, username=self.credentials['username'], password=self.credentials['password'] )
        api.service.EditProject( project_id, project_code, field_of_science, 0, project_abstract, project_title )
        return True

    def request_allocation( self, user_id, project_id, resource_id, justification, sus_requested ):
        url = re.sub( r'/api[\-a-z]*$', '/TASWebService/PortalService.asmx?wsdl', self.baseURL )
        api = Suds( url, username=self.credentials['username'], password=self.credentials['password'] )
        api.service.RequestComputeAllocation( user_id, project_id, resource_id, justification, sus_requested, 0, (0) )
        return True
