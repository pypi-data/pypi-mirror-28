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


class UserDTO(object):
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
        'parent_group_id': 'str',
        'position': 'PositionDTO',
        'identity': 'str',
        'configurable': 'bool',
        'user_groups': 'list[TenantEntity]',
        'access_policies': 'list[AccessPolicySummaryEntity]'
    }

    attribute_map = {
        'id': 'id',
        'parent_group_id': 'parentGroupId',
        'position': 'position',
        'identity': 'identity',
        'configurable': 'configurable',
        'user_groups': 'userGroups',
        'access_policies': 'accessPolicies'
    }

    def __init__(self, id=None, parent_group_id=None, position=None, identity=None, configurable=False, user_groups=None, access_policies=None):
        """
        UserDTO - a model defined in Swagger
        """

        self._id = None
        self._parent_group_id = None
        self._position = None
        self._identity = None
        self._configurable = None
        self._user_groups = None
        self._access_policies = None

        if id is not None:
          self.id = id
        if parent_group_id is not None:
          self.parent_group_id = parent_group_id
        if position is not None:
          self.position = position
        if identity is not None:
          self.identity = identity
        if configurable is not None:
          self.configurable = configurable
        if user_groups is not None:
          self.user_groups = user_groups
        if access_policies is not None:
          self.access_policies = access_policies

    @property
    def id(self):
        """
        Gets the id of this UserDTO.
        The id of the component.

        :return: The id of this UserDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserDTO.
        The id of the component.

        :param id: The id of this UserDTO.
        :type: str
        """

        self._id = id

    @property
    def parent_group_id(self):
        """
        Gets the parent_group_id of this UserDTO.
        The id of parent process group of this component if applicable.

        :return: The parent_group_id of this UserDTO.
        :rtype: str
        """
        return self._parent_group_id

    @parent_group_id.setter
    def parent_group_id(self, parent_group_id):
        """
        Sets the parent_group_id of this UserDTO.
        The id of parent process group of this component if applicable.

        :param parent_group_id: The parent_group_id of this UserDTO.
        :type: str
        """

        self._parent_group_id = parent_group_id

    @property
    def position(self):
        """
        Gets the position of this UserDTO.
        The position of this component in the UI if applicable.

        :return: The position of this UserDTO.
        :rtype: PositionDTO
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this UserDTO.
        The position of this component in the UI if applicable.

        :param position: The position of this UserDTO.
        :type: PositionDTO
        """

        self._position = position

    @property
    def identity(self):
        """
        Gets the identity of this UserDTO.
        The identity of the tenant.

        :return: The identity of this UserDTO.
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """
        Sets the identity of this UserDTO.
        The identity of the tenant.

        :param identity: The identity of this UserDTO.
        :type: str
        """

        self._identity = identity

    @property
    def configurable(self):
        """
        Gets the configurable of this UserDTO.
        Whether this tenant is configurable.

        :return: The configurable of this UserDTO.
        :rtype: bool
        """
        return self._configurable

    @configurable.setter
    def configurable(self, configurable):
        """
        Sets the configurable of this UserDTO.
        Whether this tenant is configurable.

        :param configurable: The configurable of this UserDTO.
        :type: bool
        """

        self._configurable = configurable

    @property
    def user_groups(self):
        """
        Gets the user_groups of this UserDTO.
        The groups to which the user belongs. This field is read only and it provided for convenience.

        :return: The user_groups of this UserDTO.
        :rtype: list[TenantEntity]
        """
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups):
        """
        Sets the user_groups of this UserDTO.
        The groups to which the user belongs. This field is read only and it provided for convenience.

        :param user_groups: The user_groups of this UserDTO.
        :type: list[TenantEntity]
        """

        self._user_groups = user_groups

    @property
    def access_policies(self):
        """
        Gets the access_policies of this UserDTO.
        The access policies this user belongs to.

        :return: The access_policies of this UserDTO.
        :rtype: list[AccessPolicySummaryEntity]
        """
        return self._access_policies

    @access_policies.setter
    def access_policies(self, access_policies):
        """
        Sets the access_policies of this UserDTO.
        The access policies this user belongs to.

        :param access_policies: The access_policies of this UserDTO.
        :type: list[AccessPolicySummaryEntity]
        """

        self._access_policies = access_policies

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
        if not isinstance(other, UserDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
