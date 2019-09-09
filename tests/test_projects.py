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
import mock

from pytas.models import Project

class TestProjects:

    @mock.patch('pytas.http.TASClient.project')
    def test_get(self, mock_project):
        mock_project.return_value = {
                "allocations": [
                    {
                        "computeAllocated": 50000,
                        "computeRequested": 50000,
                        "computeUsed": 52774.149,
                        "dateRequested": "2014-01-20T19:00:12Z",
                        "dateReviewed": "2014-01-20T19:00:12Z",
                        "decisionSummary": "Project Approved.",
                        "end": "2015-01-20T06:00:00Z",
                        "id": 456,
                        "justification": "Resource justification.",
                        "memoryAllocated": 0,
                        "memoryRequested": 0,
                        "project": "TEST-123456",
                        "projectId": 23567,
                        "requestor": "PI User",
                        "requestorId": 123000,
                        "resource": "Stampede3",
                        "resourceId": 31,
                        "reviewer": None,
                        "reviewerId": 0,
                        "start": "2014-01-21T06:00:00Z",
                        "status": "Active",
                        "storageAllocated": 0,
                        "storageRequested": 0
                    }
                ],
                "chargeCode": "TEST-123456",
                "description": "TEST-123456",
                "field": "Testing",
                "fieldId": 100,
                "gid": 123000,
                "id": 123,
                "pi": {
                    "citizenship": "United States",
                    "citizenshipId": 230,
                    "country": "United States",
                    "countryId": 230,
                    "department": None,
                    "departmentId": 0,
                    "email": "pi.user@example.com",
                    "emailConfirmations": [],
                    "firstName": "PI",
                    "id": 17033,
                    "institution": "University College",
                    "institutionId": 999,
                    "lastName": "User",
                    "phone": None,
                    "piEligibility": "Eligible",
                    "source": "Standard",
                    "title": None,
                    "username": "piuser"
                },
                "piId": 999999,
                "source": "Standard",
                "title": "Lorem ipsum",
                "type": "Research",
                "typeId": 0
            }

        p = Project(123)
        assert p.id == 123

    @mock.patch('pytas.http.TASClient.project')
    def test_bad_id(self, mock_project):
        mock_project.side_effect = Exception('API Error: Object reference not set to an instance of an object.')

        with pytest.raises(Exception) as e:
            p = Project(123)
            assert 'API Error' in str(e.value)
