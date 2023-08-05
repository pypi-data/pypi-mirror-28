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


class AboutDTO(object):
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
        'title': 'str',
        'version': 'str',
        'uri': 'str',
        'content_viewer_url': 'str',
        'timezone': 'str',
        'build_tag': 'str',
        'build_revision': 'str',
        'build_branch': 'str',
        'build_timestamp': 'str'
    }

    attribute_map = {
        'title': 'title',
        'version': 'version',
        'uri': 'uri',
        'content_viewer_url': 'contentViewerUrl',
        'timezone': 'timezone',
        'build_tag': 'buildTag',
        'build_revision': 'buildRevision',
        'build_branch': 'buildBranch',
        'build_timestamp': 'buildTimestamp'
    }

    def __init__(self, title=None, version=None, uri=None, content_viewer_url=None, timezone=None, build_tag=None, build_revision=None, build_branch=None, build_timestamp=None):
        """
        AboutDTO - a model defined in Swagger
        """

        self._title = None
        self._version = None
        self._uri = None
        self._content_viewer_url = None
        self._timezone = None
        self._build_tag = None
        self._build_revision = None
        self._build_branch = None
        self._build_timestamp = None

        if title is not None:
          self.title = title
        if version is not None:
          self.version = version
        if uri is not None:
          self.uri = uri
        if content_viewer_url is not None:
          self.content_viewer_url = content_viewer_url
        if timezone is not None:
          self.timezone = timezone
        if build_tag is not None:
          self.build_tag = build_tag
        if build_revision is not None:
          self.build_revision = build_revision
        if build_branch is not None:
          self.build_branch = build_branch
        if build_timestamp is not None:
          self.build_timestamp = build_timestamp

    @property
    def title(self):
        """
        Gets the title of this AboutDTO.
        The title to be used on the page and in the about dialog.

        :return: The title of this AboutDTO.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this AboutDTO.
        The title to be used on the page and in the about dialog.

        :param title: The title of this AboutDTO.
        :type: str
        """

        self._title = title

    @property
    def version(self):
        """
        Gets the version of this AboutDTO.
        The version of this NiFi.

        :return: The version of this AboutDTO.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this AboutDTO.
        The version of this NiFi.

        :param version: The version of this AboutDTO.
        :type: str
        """

        self._version = version

    @property
    def uri(self):
        """
        Gets the uri of this AboutDTO.
        The URI for the NiFi.

        :return: The uri of this AboutDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this AboutDTO.
        The URI for the NiFi.

        :param uri: The uri of this AboutDTO.
        :type: str
        """

        self._uri = uri

    @property
    def content_viewer_url(self):
        """
        Gets the content_viewer_url of this AboutDTO.
        The URL for the content viewer if configured.

        :return: The content_viewer_url of this AboutDTO.
        :rtype: str
        """
        return self._content_viewer_url

    @content_viewer_url.setter
    def content_viewer_url(self, content_viewer_url):
        """
        Sets the content_viewer_url of this AboutDTO.
        The URL for the content viewer if configured.

        :param content_viewer_url: The content_viewer_url of this AboutDTO.
        :type: str
        """

        self._content_viewer_url = content_viewer_url

    @property
    def timezone(self):
        """
        Gets the timezone of this AboutDTO.
        The timezone of the NiFi instance.

        :return: The timezone of this AboutDTO.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this AboutDTO.
        The timezone of the NiFi instance.

        :param timezone: The timezone of this AboutDTO.
        :type: str
        """

        self._timezone = timezone

    @property
    def build_tag(self):
        """
        Gets the build_tag of this AboutDTO.
        Build tag

        :return: The build_tag of this AboutDTO.
        :rtype: str
        """
        return self._build_tag

    @build_tag.setter
    def build_tag(self, build_tag):
        """
        Sets the build_tag of this AboutDTO.
        Build tag

        :param build_tag: The build_tag of this AboutDTO.
        :type: str
        """

        self._build_tag = build_tag

    @property
    def build_revision(self):
        """
        Gets the build_revision of this AboutDTO.
        Build revision or commit hash

        :return: The build_revision of this AboutDTO.
        :rtype: str
        """
        return self._build_revision

    @build_revision.setter
    def build_revision(self, build_revision):
        """
        Sets the build_revision of this AboutDTO.
        Build revision or commit hash

        :param build_revision: The build_revision of this AboutDTO.
        :type: str
        """

        self._build_revision = build_revision

    @property
    def build_branch(self):
        """
        Gets the build_branch of this AboutDTO.
        Build branch

        :return: The build_branch of this AboutDTO.
        :rtype: str
        """
        return self._build_branch

    @build_branch.setter
    def build_branch(self, build_branch):
        """
        Sets the build_branch of this AboutDTO.
        Build branch

        :param build_branch: The build_branch of this AboutDTO.
        :type: str
        """

        self._build_branch = build_branch

    @property
    def build_timestamp(self):
        """
        Gets the build_timestamp of this AboutDTO.
        Build timestamp

        :return: The build_timestamp of this AboutDTO.
        :rtype: str
        """
        return self._build_timestamp

    @build_timestamp.setter
    def build_timestamp(self, build_timestamp):
        """
        Sets the build_timestamp of this AboutDTO.
        Build timestamp

        :param build_timestamp: The build_timestamp of this AboutDTO.
        :type: str
        """

        self._build_timestamp = build_timestamp

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
        if not isinstance(other, AboutDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
