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

from pytas.pytas import client

@pytest.fixture
def tas():
    return client()

class TestTAS:

    def test_auth(self, tas):
        username = os.environ.get('TAS_USERNAME')
        password = os.environ.get('TAS_PASSWORD')
        resp = tas.authenticate(username, password)
        assert resp['status'] == 'success', "API call successful"
        assert resp['result'], "Authentication successful"

    def test_authfail(self, tas):
        resp = tas.authenticate('bad','username')
        assert resp['status'] == 'error', "API call successful"
        assert not resp['result'], "Authentication failed"
