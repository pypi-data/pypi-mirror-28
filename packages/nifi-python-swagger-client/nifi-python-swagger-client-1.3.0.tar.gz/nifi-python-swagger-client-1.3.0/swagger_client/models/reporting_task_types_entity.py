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


class ReportingTaskTypesEntity(object):
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
        'reporting_task_types': 'list[DocumentedTypeDTO]'
    }

    attribute_map = {
        'reporting_task_types': 'reportingTaskTypes'
    }

    def __init__(self, reporting_task_types=None):
        """
        ReportingTaskTypesEntity - a model defined in Swagger
        """

        self._reporting_task_types = None

        if reporting_task_types is not None:
          self.reporting_task_types = reporting_task_types

    @property
    def reporting_task_types(self):
        """
        Gets the reporting_task_types of this ReportingTaskTypesEntity.

        :return: The reporting_task_types of this ReportingTaskTypesEntity.
        :rtype: list[DocumentedTypeDTO]
        """
        return self._reporting_task_types

    @reporting_task_types.setter
    def reporting_task_types(self, reporting_task_types):
        """
        Sets the reporting_task_types of this ReportingTaskTypesEntity.

        :param reporting_task_types: The reporting_task_types of this ReportingTaskTypesEntity.
        :type: list[DocumentedTypeDTO]
        """

        self._reporting_task_types = reporting_task_types

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
        if not isinstance(other, ReportingTaskTypesEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
