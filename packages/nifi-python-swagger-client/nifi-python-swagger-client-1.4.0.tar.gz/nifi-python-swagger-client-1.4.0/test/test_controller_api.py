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
from swagger_client.apis.controller_api import ControllerApi


class TestControllerApi(unittest.TestCase):
    """ ControllerApi unit test stubs """

    def setUp(self):
        self.api = swagger_client.apis.controller_api.ControllerApi()

    def tearDown(self):
        pass

    def test_create_bulletin(self):
        """
        Test case for create_bulletin

        Creates a new bulletin
        """
        pass

    def test_create_controller_service(self):
        """
        Test case for create_controller_service

        Creates a new controller service
        """
        pass

    def test_create_reporting_task(self):
        """
        Test case for create_reporting_task

        Creates a new reporting task
        """
        pass

    def test_delete_history(self):
        """
        Test case for delete_history

        Purges history
        """
        pass

    def test_delete_node(self):
        """
        Test case for delete_node

        Removes a node from the cluster
        """
        pass

    def test_get_cluster(self):
        """
        Test case for get_cluster

        Gets the contents of the cluster
        """
        pass

    def test_get_controller_config(self):
        """
        Test case for get_controller_config

        Retrieves the configuration for this NiFi Controller
        """
        pass

    def test_get_node(self):
        """
        Test case for get_node

        Gets a node in the cluster
        """
        pass

    def test_update_controller_config(self):
        """
        Test case for update_controller_config

        Retrieves the configuration for this NiFi
        """
        pass

    def test_update_node(self):
        """
        Test case for update_node

        Updates a node in the cluster
        """
        pass


if __name__ == '__main__':
    unittest.main()
