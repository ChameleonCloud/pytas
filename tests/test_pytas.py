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

from pytas.http import TASClient

@pytest.fixture
def tas():
    return TASClient()

class TestTAS:

    def test_auth(self, tas):
        username = os.environ.get('TAS_USERNAME')
        password = os.environ.get('TAS_PASSWORD')
        assert tas.authenticate(username, password)

    def test_auth_bad_username(self, tas):
        with pytest.raises(Exception):
            tas.authenticate('bad','username')

    def test_auth_bad_password(self, tas):
        assert not tas.authenticate('mrhanlon','badpassword')

    def test_get_user_by_username(self, tas):
        resp = tas.get_user(username='mrhanlon')
        assert resp['username'] == 'mrhanlon'

    def test_get_institutions(self, tas):
        resp = tas.institutions()
        assert resp is not None

    def test_get_institution_by_id(self, tas):
        resp = tas.get_institution(1)
        assert resp is not None

    def test_get_institution_departments_by_id(self, tas):
        resp = tas.get_departments(1)
        assert resp is not None

    def test_get_department_by_id(self, tas):
        resp = tas.get_department(1, 127)
        assert resp is not None

    def test_get_countries(self, tas):
        resp = tas.countries()
        assert resp is not None
