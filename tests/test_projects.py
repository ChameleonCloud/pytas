#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_projects
----------------------------------

Tests for `Projects` module.
"""

import os
import pytest
import json
import httpretty

from pytas.models import Project

class TestProjects:

    @httpretty.activate
    def test_get(self):
        json_response = """
        {
            "message": null,
            "result": {
                "allocations": [
                    {
                        "computeAllocated": 50000,
                        "computeRequested": 50000,
                        "computeUsed": 52774.149,
                        "dateRequested": "2014-01-20T19:00:12Z",
                        "dateReviewed": "2014-01-20T19:00:12Z",
                        "decisionSummary": "Automatic TG AMIE approval.",
                        "end": "2015-01-20T06:00:00Z",
                        "id": 22119,
                        "justification": "TeraGrid 'New' allocation.",
                        "memoryAllocated": 0,
                        "memoryRequested": 0,
                        "project": "TG-MCB140064",
                        "projectId": 23567,
                        "requestor": "Lane Votapka",
                        "requestorId": 17033,
                        "resource": "Stampede3",
                        "resourceId": 31,
                        "reviewer": null,
                        "reviewerId": 0,
                        "start": "2014-01-21T06:00:00Z",
                        "status": "Active",
                        "storageAllocated": 0,
                        "storageRequested": 0
                    }
                ],
                "chargeCode": "lorem-ipsum",
                "description": "Lorem ipsum.",
                "field": "Biophysics",
                "fieldId": 105,
                "gid": 123000,
                "id": 123,
                "pi": {
                    "citizenship": "United States",
                    "citizenshipId": 230,
                    "country": "United States",
                    "countryId": 230,
                    "department": null,
                    "departmentId": 0,
                    "email": "pi.user@example.com",
                    "emailConfirmations": [],
                    "firstName": "PI",
                    "id": 17033,
                    "institution": "University College",
                    "institutionId": 999,
                    "lastName": "User",
                    "phone": null,
                    "piEligibility": "Eligible",
                    "source": "Standard",
                    "title": null,
                    "username": "piuser"
                },
                "piId": 999999,
                "source": "Standard",
                "title": "Lorem ipsum",
                "type": "Research",
                "typeId": 0
            },
            "status": "success"
        }
        """
        httpretty.register_uri(httpretty.GET,
                               'https://example.com/api/v1/projects/123',
                               body=json_response, content_type='application/json')

        p = Project(123)
        assert p.id == 123

    @httpretty.activate
    def test_bad_id(self):
        httpretty.register_uri(httpretty.GET,
                               'https://example.com/api/v1/projects/123',
                               body='{"status":"error","result":null,"message":"Does not exist"}',
                               content_type='application/json')

        with pytest.raises(Exception) as e:
            p = Project(123)
            assert 'Does not exist' in str(e.value)