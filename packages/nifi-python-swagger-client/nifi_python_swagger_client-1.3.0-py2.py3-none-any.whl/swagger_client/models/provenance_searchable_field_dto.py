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


class ProvenanceSearchableFieldDTO(object):
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
        'id': 'str',
        'field': 'str',
        'label': 'str',
        'type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'field': 'field',
        'label': 'label',
        'type': 'type'
    }

    def __init__(self, id=None, field=None, label=None, type=None):
        """
        ProvenanceSearchableFieldDTO - a model defined in Swagger
        """

        self._id = None
        self._field = None
        self._label = None
        self._type = None

        if id is not None:
          self.id = id
        if field is not None:
          self.field = field
        if label is not None:
          self.label = label
        if type is not None:
          self.type = type

    @property
    def id(self):
        """
        Gets the id of this ProvenanceSearchableFieldDTO.
        The id of the searchable field.

        :return: The id of this ProvenanceSearchableFieldDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProvenanceSearchableFieldDTO.
        The id of the searchable field.

        :param id: The id of this ProvenanceSearchableFieldDTO.
        :type: str
        """

        self._id = id

    @property
    def field(self):
        """
        Gets the field of this ProvenanceSearchableFieldDTO.
        The searchable field.

        :return: The field of this ProvenanceSearchableFieldDTO.
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """
        Sets the field of this ProvenanceSearchableFieldDTO.
        The searchable field.

        :param field: The field of this ProvenanceSearchableFieldDTO.
        :type: str
        """

        self._field = field

    @property
    def label(self):
        """
        Gets the label of this ProvenanceSearchableFieldDTO.
        The label for the searchable field.

        :return: The label of this ProvenanceSearchableFieldDTO.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        Sets the label of this ProvenanceSearchableFieldDTO.
        The label for the searchable field.

        :param label: The label of this ProvenanceSearchableFieldDTO.
        :type: str
        """

        self._label = label

    @property
    def type(self):
        """
        Gets the type of this ProvenanceSearchableFieldDTO.
        The type of the searchable field.

        :return: The type of this ProvenanceSearchableFieldDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ProvenanceSearchableFieldDTO.
        The type of the searchable field.

        :param type: The type of this ProvenanceSearchableFieldDTO.
        :type: str
        """

        self._type = type

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
        if not isinstance(other, ProvenanceSearchableFieldDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
