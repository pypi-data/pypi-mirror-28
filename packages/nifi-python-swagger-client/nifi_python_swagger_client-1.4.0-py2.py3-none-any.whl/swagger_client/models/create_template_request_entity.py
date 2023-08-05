# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.4.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class CreateTemplateRequestEntity(object):
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
        'name': 'str',
        'description': 'str',
        'snippet_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'snippet_id': 'snippetId'
    }

    def __init__(self, name=None, description=None, snippet_id=None):
        """
        CreateTemplateRequestEntity - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._snippet_id = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if snippet_id is not None:
          self.snippet_id = snippet_id

    @property
    def name(self):
        """
        Gets the name of this CreateTemplateRequestEntity.
        The name of the template.

        :return: The name of this CreateTemplateRequestEntity.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateTemplateRequestEntity.
        The name of the template.

        :param name: The name of this CreateTemplateRequestEntity.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CreateTemplateRequestEntity.
        The description of the template.

        :return: The description of this CreateTemplateRequestEntity.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateTemplateRequestEntity.
        The description of the template.

        :param description: The description of this CreateTemplateRequestEntity.
        :type: str
        """

        self._description = description

    @property
    def snippet_id(self):
        """
        Gets the snippet_id of this CreateTemplateRequestEntity.
        The identifier of the snippet.

        :return: The snippet_id of this CreateTemplateRequestEntity.
        :rtype: str
        """
        return self._snippet_id

    @snippet_id.setter
    def snippet_id(self, snippet_id):
        """
        Sets the snippet_id of this CreateTemplateRequestEntity.
        The identifier of the snippet.

        :param snippet_id: The snippet_id of this CreateTemplateRequestEntity.
        :type: str
        """

        self._snippet_id = snippet_id

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
        if not isinstance(other, CreateTemplateRequestEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
