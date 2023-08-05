# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.2.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.models.process_group_flow_entity import ProcessGroupFlowEntity


class TestProcessGroupFlowEntity(unittest.TestCase):
    """ ProcessGroupFlowEntity unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessGroupFlowEntity(self):
        """
        Test ProcessGroupFlowEntity
        """
        # FIXME: construct object with mandatory attributes with example values
        #model = swagger_client.models.process_group_flow_entity.ProcessGroupFlowEntity()
        pass


if __name__ == '__main__':
    unittest.main()
