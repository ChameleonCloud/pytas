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
        assert tas.authenticate(username, password)

    def test_auth_bad_username(self, tas):
        with pytest.raises(Exception):
            tas.authenticate('bad','username')

    def test_auth_bad_password(self, tas):
        assert not tas.authenticate('mrhanlon','badpassword')
