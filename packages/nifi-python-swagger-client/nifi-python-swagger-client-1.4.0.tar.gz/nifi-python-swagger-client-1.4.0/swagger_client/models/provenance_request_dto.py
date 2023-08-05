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


class ProvenanceRequestDTO(object):
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
        'search_terms': 'dict(str, str)',
        'cluster_node_id': 'str',
        'start_date': 'str',
        'end_date': 'str',
        'minimum_file_size': 'str',
        'maximum_file_size': 'str',
        'max_results': 'int',
        'summarize': 'bool',
        'incremental_results': 'bool'
    }

    attribute_map = {
        'search_terms': 'searchTerms',
        'cluster_node_id': 'clusterNodeId',
        'start_date': 'startDate',
        'end_date': 'endDate',
        'minimum_file_size': 'minimumFileSize',
        'maximum_file_size': 'maximumFileSize',
        'max_results': 'maxResults',
        'summarize': 'summarize',
        'incremental_results': 'incrementalResults'
    }

    def __init__(self, search_terms=None, cluster_node_id=None, start_date=None, end_date=None, minimum_file_size=None, maximum_file_size=None, max_results=None, summarize=False, incremental_results=False):
        """
        ProvenanceRequestDTO - a model defined in Swagger
        """

        self._search_terms = None
        self._cluster_node_id = None
        self._start_date = None
        self._end_date = None
        self._minimum_file_size = None
        self._maximum_file_size = None
        self._max_results = None
        self._summarize = None
        self._incremental_results = None

        if search_terms is not None:
          self.search_terms = search_terms
        if cluster_node_id is not None:
          self.cluster_node_id = cluster_node_id
        if start_date is not None:
          self.start_date = start_date
        if end_date is not None:
          self.end_date = end_date
        if minimum_file_size is not None:
          self.minimum_file_size = minimum_file_size
        if maximum_file_size is not None:
          self.maximum_file_size = maximum_file_size
        if max_results is not None:
          self.max_results = max_results
        if summarize is not None:
          self.summarize = summarize
        if incremental_results is not None:
          self.incremental_results = incremental_results

    @property
    def search_terms(self):
        """
        Gets the search_terms of this ProvenanceRequestDTO.
        The search terms used to perform the search.

        :return: The search_terms of this ProvenanceRequestDTO.
        :rtype: dict(str, str)
        """
        return self._search_terms

    @search_terms.setter
    def search_terms(self, search_terms):
        """
        Sets the search_terms of this ProvenanceRequestDTO.
        The search terms used to perform the search.

        :param search_terms: The search_terms of this ProvenanceRequestDTO.
        :type: dict(str, str)
        """

        self._search_terms = search_terms

    @property
    def cluster_node_id(self):
        """
        Gets the cluster_node_id of this ProvenanceRequestDTO.
        The id of the node in the cluster where this provenance originated.

        :return: The cluster_node_id of this ProvenanceRequestDTO.
        :rtype: str
        """
        return self._cluster_node_id

    @cluster_node_id.setter
    def cluster_node_id(self, cluster_node_id):
        """
        Sets the cluster_node_id of this ProvenanceRequestDTO.
        The id of the node in the cluster where this provenance originated.

        :param cluster_node_id: The cluster_node_id of this ProvenanceRequestDTO.
        :type: str
        """

        self._cluster_node_id = cluster_node_id

    @property
    def start_date(self):
        """
        Gets the start_date of this ProvenanceRequestDTO.
        The earliest event time to include in the query.

        :return: The start_date of this ProvenanceRequestDTO.
        :rtype: str
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this ProvenanceRequestDTO.
        The earliest event time to include in the query.

        :param start_date: The start_date of this ProvenanceRequestDTO.
        :type: str
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this ProvenanceRequestDTO.
        The latest event time to include in the query.

        :return: The end_date of this ProvenanceRequestDTO.
        :rtype: str
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this ProvenanceRequestDTO.
        The latest event time to include in the query.

        :param end_date: The end_date of this ProvenanceRequestDTO.
        :type: str
        """

        self._end_date = end_date

    @property
    def minimum_file_size(self):
        """
        Gets the minimum_file_size of this ProvenanceRequestDTO.
        The minimum file size to include in the query.

        :return: The minimum_file_size of this ProvenanceRequestDTO.
        :rtype: str
        """
        return self._minimum_file_size

    @minimum_file_size.setter
    def minimum_file_size(self, minimum_file_size):
        """
        Sets the minimum_file_size of this ProvenanceRequestDTO.
        The minimum file size to include in the query.

        :param minimum_file_size: The minimum_file_size of this ProvenanceRequestDTO.
        :type: str
        """

        self._minimum_file_size = minimum_file_size

    @property
    def maximum_file_size(self):
        """
        Gets the maximum_file_size of this ProvenanceRequestDTO.
        The maximum file size to include in the query.

        :return: The maximum_file_size of this ProvenanceRequestDTO.
        :rtype: str
        """
        return self._maximum_file_size

    @maximum_file_size.setter
    def maximum_file_size(self, maximum_file_size):
        """
        Sets the maximum_file_size of this ProvenanceRequestDTO.
        The maximum file size to include in the query.

        :param maximum_file_size: The maximum_file_size of this ProvenanceRequestDTO.
        :type: str
        """

        self._maximum_file_size = maximum_file_size

    @property
    def max_results(self):
        """
        Gets the max_results of this ProvenanceRequestDTO.
        The maximum number of results to include.

        :return: The max_results of this ProvenanceRequestDTO.
        :rtype: int
        """
        return self._max_results

    @max_results.setter
    def max_results(self, max_results):
        """
        Sets the max_results of this ProvenanceRequestDTO.
        The maximum number of results to include.

        :param max_results: The max_results of this ProvenanceRequestDTO.
        :type: int
        """

        self._max_results = max_results

    @property
    def summarize(self):
        """
        Gets the summarize of this ProvenanceRequestDTO.
        Whether or not to summarize provenance events returned. This property is false by default.

        :return: The summarize of this ProvenanceRequestDTO.
        :rtype: bool
        """
        return self._summarize

    @summarize.setter
    def summarize(self, summarize):
        """
        Sets the summarize of this ProvenanceRequestDTO.
        Whether or not to summarize provenance events returned. This property is false by default.

        :param summarize: The summarize of this ProvenanceRequestDTO.
        :type: bool
        """

        self._summarize = summarize

    @property
    def incremental_results(self):
        """
        Gets the incremental_results of this ProvenanceRequestDTO.
        Whether or not incremental results are returned. If false, provenance events are only returned once the query completes. This property is true by default.

        :return: The incremental_results of this ProvenanceRequestDTO.
        :rtype: bool
        """
        return self._incremental_results

    @incremental_results.setter
    def incremental_results(self, incremental_results):
        """
        Sets the incremental_results of this ProvenanceRequestDTO.
        Whether or not incremental results are returned. If false, provenance events are only returned once the query completes. This property is true by default.

        :param incremental_results: The incremental_results of this ProvenanceRequestDTO.
        :type: bool
        """

        self._incremental_results = incremental_results

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
        if not isinstance(other, ProvenanceRequestDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
