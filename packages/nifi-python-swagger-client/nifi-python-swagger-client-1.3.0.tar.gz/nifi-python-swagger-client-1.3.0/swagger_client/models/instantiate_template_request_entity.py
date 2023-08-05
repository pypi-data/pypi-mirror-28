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


class InstantiateTemplateRequestEntity(object):
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
        'origin_x': 'float',
        'origin_y': 'float',
        'template_id': 'str',
        'encoding_version': 'str',
        'snippet': 'FlowSnippetDTO'
    }

    attribute_map = {
        'origin_x': 'originX',
        'origin_y': 'originY',
        'template_id': 'templateId',
        'encoding_version': 'encodingVersion',
        'snippet': 'snippet'
    }

    def __init__(self, origin_x=None, origin_y=None, template_id=None, encoding_version=None, snippet=None):
        """
        InstantiateTemplateRequestEntity - a model defined in Swagger
        """

        self._origin_x = None
        self._origin_y = None
        self._template_id = None
        self._encoding_version = None
        self._snippet = None

        if origin_x is not None:
          self.origin_x = origin_x
        if origin_y is not None:
          self.origin_y = origin_y
        if template_id is not None:
          self.template_id = template_id
        if encoding_version is not None:
          self.encoding_version = encoding_version
        if snippet is not None:
          self.snippet = snippet

    @property
    def origin_x(self):
        """
        Gets the origin_x of this InstantiateTemplateRequestEntity.
        The x coordinate of the origin of the bounding box where the new components will be placed.

        :return: The origin_x of this InstantiateTemplateRequestEntity.
        :rtype: float
        """
        return self._origin_x

    @origin_x.setter
    def origin_x(self, origin_x):
        """
        Sets the origin_x of this InstantiateTemplateRequestEntity.
        The x coordinate of the origin of the bounding box where the new components will be placed.

        :param origin_x: The origin_x of this InstantiateTemplateRequestEntity.
        :type: float
        """

        self._origin_x = origin_x

    @property
    def origin_y(self):
        """
        Gets the origin_y of this InstantiateTemplateRequestEntity.
        The y coordinate of the origin of the bounding box where the new components will be placed.

        :return: The origin_y of this InstantiateTemplateRequestEntity.
        :rtype: float
        """
        return self._origin_y

    @origin_y.setter
    def origin_y(self, origin_y):
        """
        Sets the origin_y of this InstantiateTemplateRequestEntity.
        The y coordinate of the origin of the bounding box where the new components will be placed.

        :param origin_y: The origin_y of this InstantiateTemplateRequestEntity.
        :type: float
        """

        self._origin_y = origin_y

    @property
    def template_id(self):
        """
        Gets the template_id of this InstantiateTemplateRequestEntity.
        The identifier of the template.

        :return: The template_id of this InstantiateTemplateRequestEntity.
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """
        Sets the template_id of this InstantiateTemplateRequestEntity.
        The identifier of the template.

        :param template_id: The template_id of this InstantiateTemplateRequestEntity.
        :type: str
        """

        self._template_id = template_id

    @property
    def encoding_version(self):
        """
        Gets the encoding_version of this InstantiateTemplateRequestEntity.
        The encoding version of the flow snippet. If not specified, this is automatically populated by the node receiving the user request. If the snippet is specified, the version will be the latest. If the snippet is not specified, the version will come from the underlying template. These details need to be replicated throughout the cluster to ensure consistency.

        :return: The encoding_version of this InstantiateTemplateRequestEntity.
        :rtype: str
        """
        return self._encoding_version

    @encoding_version.setter
    def encoding_version(self, encoding_version):
        """
        Sets the encoding_version of this InstantiateTemplateRequestEntity.
        The encoding version of the flow snippet. If not specified, this is automatically populated by the node receiving the user request. If the snippet is specified, the version will be the latest. If the snippet is not specified, the version will come from the underlying template. These details need to be replicated throughout the cluster to ensure consistency.

        :param encoding_version: The encoding_version of this InstantiateTemplateRequestEntity.
        :type: str
        """

        self._encoding_version = encoding_version

    @property
    def snippet(self):
        """
        Gets the snippet of this InstantiateTemplateRequestEntity.
        A flow snippet of the template contents. If not specified, this is automatically populated by the node receiving the user request. These details need to be replicated throughout the cluster to ensure consistency.

        :return: The snippet of this InstantiateTemplateRequestEntity.
        :rtype: FlowSnippetDTO
        """
        return self._snippet

    @snippet.setter
    def snippet(self, snippet):
        """
        Sets the snippet of this InstantiateTemplateRequestEntity.
        A flow snippet of the template contents. If not specified, this is automatically populated by the node receiving the user request. These details need to be replicated throughout the cluster to ensure consistency.

        :param snippet: The snippet of this InstantiateTemplateRequestEntity.
        :type: FlowSnippetDTO
        """

        self._snippet = snippet

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
        if not isinstance(other, InstantiateTemplateRequestEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
