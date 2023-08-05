# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.3.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class FlowConfigurationEntity(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'flow_configuration': 'FlowConfigurationDTO'
    }

    attribute_map = {
        'flow_configuration': 'flowConfiguration'
    }

    def __init__(self, flow_configuration=None):
        """
        FlowConfigurationEntity - a model defined in Swagger
        """

        self._flow_configuration = None

        if flow_configuration is not None:
          self.flow_configuration = flow_configuration

    @property
    def flow_configuration(self):
        """
        Gets the flow_configuration of this FlowConfigurationEntity.
        The controller configuration.

        :return: The flow_configuration of this FlowConfigurationEntity.
        :rtype: FlowConfigurationDTO
        """
        return self._flow_configuration

    @flow_configuration.setter
    def flow_configuration(self, flow_configuration):
        """
        Sets the flow_configuration of this FlowConfigurationEntity.
        The controller configuration.

        :param flow_configuration: The flow_configuration of this FlowConfigurationEntity.
        :type: FlowConfigurationDTO
        """

        self._flow_configuration = flow_configuration

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, FlowConfigurationEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
