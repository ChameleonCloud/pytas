#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pytas
----------------------------------

Tests for `pytas` module.
"""

import os
import pytest
import json
import responses

from pytas.http import TASClient

@pytest.fixture
def tas():
    return TASClient()

class TestTAS:

    @responses.activate
    def test_auth(self, tas):
        responses.add(responses.POST, 'https://example.com/api/auth/login',
                  json={"status": "success", "result": "true"}, status=200)

        assert tas.authenticate('username', 'password')

    @responses.activate
    def test_auth_bad_username(self, tas):
        responses.add(responses.POST, 'https://example.com/api/auth/login',
            json={"status": "success", "result": None,
                  "message": "The username or password is incorrect."},
            status=200)

        with pytest.raises(Exception) as e:
            tas.authenticate('bad','username')
            assert "The username or password is incorrect." in e.value

    @responses.activate
    def test_auth_bad_password(self, tas):
        responses.add(responses.POST, 'https://example.com/api/auth/login',
            json={"status": "success", "result": False, "message": ""},
            status=200)

        assert not tas.authenticate('mrhanlon','badpassword')

    @responses.activate
    def test_get_user_by_username(self, tas):
        responses.add(responses.GET, 'https://example.com/api/v1/users/username/mrhanlon',
            json={
                "status": "success",
                "result": {"username": "mrhanlon"},
                "message": ""
            },
            status=200)

        resp = tas.get_user(username='mrhanlon')
        assert resp['username'] == 'mrhanlon'

    @responses.activate
    def test_get_institutions(self, tas):
        responses.add(responses.GET, 'https://example.com/api/v1/institutions/',
            json={
                "status": "success",
                "result": [
                    {"id": 1, "name": "University of Texas at Austin", "departments": []},
                    {"id": 2, "name": "School of Architecture", "departments": []}
                ],
                "message": ""
            },
            status=200)

        resp = tas.institutions()
        assert resp is not None
        assert len(resp) == 2

    @responses.activate
    def test_get_institution_by_id(self, tas):
        responses.add(responses.GET, 'https://example.com/api/v1/institutions/1',
            json={
                "status": "success",
                "result": {
                    "id": 1,
                    "name": "University of Texas at Austin",
                    "departments": []
                },
                "message": ""
            },
            status=200)

        resp = tas.get_institution(1)
        assert resp is not None
        assert resp['id'] == 1

    @responses.activate
    def test_get_institution_departments_by_id(self, tas):
        responses.add(responses.GET, 'https://example.com/api/v1/institutions/1/departments',
            json={
                "status": "success",
                "result": [
                    {
                        "id": 125,
                        "name": "ACES IT Group"
                    },
                    {
                        "id": 128,
                        "name": "Advanced Manufacturing Center"
                    },
                    {
                        "id": 76,
                        "name": "Americo Paredes Center for Cultural Studies"
                    },
                ],
                "message": ""
            },
            status=200)

        resp = tas.get_departments(1)
        assert resp is not None
        assert len(resp) == 3

    @responses.activate
    def test_get_department_by_id(self, tas):
        responses.add(responses.GET, 'https://example.com/api/v1/institutions/127',
            json={
                "status": "success",
                "result": {
                        "id": 127,
                        "name": "Texas Advanced Computing Center",
                        "departments": []
                },
                "message": ""
            },
            status=200)

        resp = tas.get_department(1, 127)
        assert resp is not None
        assert resp['name'] == 'Texas Advanced Computing Center'

    # @responses.activate
    # def test_get_countries(self, tas):
    #     resp = tas.countries()
    #     assert resp is not None
