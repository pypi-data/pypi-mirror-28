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


class FlowDTO(object):
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
        'process_groups': 'list[ProcessGroupEntity]',
        'remote_process_groups': 'list[RemoteProcessGroupEntity]',
        'processors': 'list[ProcessorEntity]',
        'input_ports': 'list[PortEntity]',
        'output_ports': 'list[PortEntity]',
        'connections': 'list[ConnectionEntity]',
        'labels': 'list[LabelEntity]',
        'funnels': 'list[FunnelEntity]'
    }

    attribute_map = {
        'process_groups': 'processGroups',
        'remote_process_groups': 'remoteProcessGroups',
        'processors': 'processors',
        'input_ports': 'inputPorts',
        'output_ports': 'outputPorts',
        'connections': 'connections',
        'labels': 'labels',
        'funnels': 'funnels'
    }

    def __init__(self, process_groups=None, remote_process_groups=None, processors=None, input_ports=None, output_ports=None, connections=None, labels=None, funnels=None):
        """
        FlowDTO - a model defined in Swagger
        """

        self._process_groups = None
        self._remote_process_groups = None
        self._processors = None
        self._input_ports = None
        self._output_ports = None
        self._connections = None
        self._labels = None
        self._funnels = None

        if process_groups is not None:
          self.process_groups = process_groups
        if remote_process_groups is not None:
          self.remote_process_groups = remote_process_groups
        if processors is not None:
          self.processors = processors
        if input_ports is not None:
          self.input_ports = input_ports
        if output_ports is not None:
          self.output_ports = output_ports
        if connections is not None:
          self.connections = connections
        if labels is not None:
          self.labels = labels
        if funnels is not None:
          self.funnels = funnels

    @property
    def process_groups(self):
        """
        Gets the process_groups of this FlowDTO.
        The process groups in this flow.

        :return: The process_groups of this FlowDTO.
        :rtype: list[ProcessGroupEntity]
        """
        return self._process_groups

    @process_groups.setter
    def process_groups(self, process_groups):
        """
        Sets the process_groups of this FlowDTO.
        The process groups in this flow.

        :param process_groups: The process_groups of this FlowDTO.
        :type: list[ProcessGroupEntity]
        """

        self._process_groups = process_groups

    @property
    def remote_process_groups(self):
        """
        Gets the remote_process_groups of this FlowDTO.
        The remote process groups in this flow.

        :return: The remote_process_groups of this FlowDTO.
        :rtype: list[RemoteProcessGroupEntity]
        """
        return self._remote_process_groups

    @remote_process_groups.setter
    def remote_process_groups(self, remote_process_groups):
        """
        Sets the remote_process_groups of this FlowDTO.
        The remote process groups in this flow.

        :param remote_process_groups: The remote_process_groups of this FlowDTO.
        :type: list[RemoteProcessGroupEntity]
        """

        self._remote_process_groups = remote_process_groups

    @property
    def processors(self):
        """
        Gets the processors of this FlowDTO.
        The processors in this flow.

        :return: The processors of this FlowDTO.
        :rtype: list[ProcessorEntity]
        """
        return self._processors

    @processors.setter
    def processors(self, processors):
        """
        Sets the processors of this FlowDTO.
        The processors in this flow.

        :param processors: The processors of this FlowDTO.
        :type: list[ProcessorEntity]
        """

        self._processors = processors

    @property
    def input_ports(self):
        """
        Gets the input_ports of this FlowDTO.
        The input ports in this flow.

        :return: The input_ports of this FlowDTO.
        :rtype: list[PortEntity]
        """
        return self._input_ports

    @input_ports.setter
    def input_ports(self, input_ports):
        """
        Sets the input_ports of this FlowDTO.
        The input ports in this flow.

        :param input_ports: The input_ports of this FlowDTO.
        :type: list[PortEntity]
        """

        self._input_ports = input_ports

    @property
    def output_ports(self):
        """
        Gets the output_ports of this FlowDTO.
        The output ports in this flow.

        :return: The output_ports of this FlowDTO.
        :rtype: list[PortEntity]
        """
        return self._output_ports

    @output_ports.setter
    def output_ports(self, output_ports):
        """
        Sets the output_ports of this FlowDTO.
        The output ports in this flow.

        :param output_ports: The output_ports of this FlowDTO.
        :type: list[PortEntity]
        """

        self._output_ports = output_ports

    @property
    def connections(self):
        """
        Gets the connections of this FlowDTO.
        The connections in this flow.

        :return: The connections of this FlowDTO.
        :rtype: list[ConnectionEntity]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """
        Sets the connections of this FlowDTO.
        The connections in this flow.

        :param connections: The connections of this FlowDTO.
        :type: list[ConnectionEntity]
        """

        self._connections = connections

    @property
    def labels(self):
        """
        Gets the labels of this FlowDTO.
        The labels in this flow.

        :return: The labels of this FlowDTO.
        :rtype: list[LabelEntity]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this FlowDTO.
        The labels in this flow.

        :param labels: The labels of this FlowDTO.
        :type: list[LabelEntity]
        """

        self._labels = labels

    @property
    def funnels(self):
        """
        Gets the funnels of this FlowDTO.
        The funnels in this flow.

        :return: The funnels of this FlowDTO.
        :rtype: list[FunnelEntity]
        """
        return self._funnels

    @funnels.setter
    def funnels(self, funnels):
        """
        Sets the funnels of this FlowDTO.
        The funnels in this flow.

        :param funnels: The funnels of this FlowDTO.
        :type: list[FunnelEntity]
        """

        self._funnels = funnels

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
        if not isinstance(other, FlowDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
