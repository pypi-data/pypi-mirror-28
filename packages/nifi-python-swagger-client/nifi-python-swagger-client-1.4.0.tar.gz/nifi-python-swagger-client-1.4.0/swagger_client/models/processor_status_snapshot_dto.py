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


class ProcessorStatusSnapshotDTO(object):
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
        'group_id': 'str',
        'name': 'str',
        'type': 'str',
        'run_status': 'str',
        'bytes_read': 'int',
        'bytes_written': 'int',
        'read': 'str',
        'written': 'str',
        'flow_files_in': 'int',
        'bytes_in': 'int',
        'input': 'str',
        'flow_files_out': 'int',
        'bytes_out': 'int',
        'output': 'str',
        'task_count': 'int',
        'tasks_duration_nanos': 'int',
        'tasks': 'str',
        'tasks_duration': 'str',
        'active_thread_count': 'int'
    }

    attribute_map = {
        'id': 'id',
        'group_id': 'groupId',
        'name': 'name',
        'type': 'type',
        'run_status': 'runStatus',
        'bytes_read': 'bytesRead',
        'bytes_written': 'bytesWritten',
        'read': 'read',
        'written': 'written',
        'flow_files_in': 'flowFilesIn',
        'bytes_in': 'bytesIn',
        'input': 'input',
        'flow_files_out': 'flowFilesOut',
        'bytes_out': 'bytesOut',
        'output': 'output',
        'task_count': 'taskCount',
        'tasks_duration_nanos': 'tasksDurationNanos',
        'tasks': 'tasks',
        'tasks_duration': 'tasksDuration',
        'active_thread_count': 'activeThreadCount'
    }

    def __init__(self, id=None, group_id=None, name=None, type=None, run_status=None, bytes_read=None, bytes_written=None, read=None, written=None, flow_files_in=None, bytes_in=None, input=None, flow_files_out=None, bytes_out=None, output=None, task_count=None, tasks_duration_nanos=None, tasks=None, tasks_duration=None, active_thread_count=None):
        """
        ProcessorStatusSnapshotDTO - a model defined in Swagger
        """

        self._id = None
        self._group_id = None
        self._name = None
        self._type = None
        self._run_status = None
        self._bytes_read = None
        self._bytes_written = None
        self._read = None
        self._written = None
        self._flow_files_in = None
        self._bytes_in = None
        self._input = None
        self._flow_files_out = None
        self._bytes_out = None
        self._output = None
        self._task_count = None
        self._tasks_duration_nanos = None
        self._tasks = None
        self._tasks_duration = None
        self._active_thread_count = None

        if id is not None:
          self.id = id
        if group_id is not None:
          self.group_id = group_id
        if name is not None:
          self.name = name
        if type is not None:
          self.type = type
        if run_status is not None:
          self.run_status = run_status
        if bytes_read is not None:
          self.bytes_read = bytes_read
        if bytes_written is not None:
          self.bytes_written = bytes_written
        if read is not None:
          self.read = read
        if written is not None:
          self.written = written
        if flow_files_in is not None:
          self.flow_files_in = flow_files_in
        if bytes_in is not None:
          self.bytes_in = bytes_in
        if input is not None:
          self.input = input
        if flow_files_out is not None:
          self.flow_files_out = flow_files_out
        if bytes_out is not None:
          self.bytes_out = bytes_out
        if output is not None:
          self.output = output
        if task_count is not None:
          self.task_count = task_count
        if tasks_duration_nanos is not None:
          self.tasks_duration_nanos = tasks_duration_nanos
        if tasks is not None:
          self.tasks = tasks
        if tasks_duration is not None:
          self.tasks_duration = tasks_duration
        if active_thread_count is not None:
          self.active_thread_count = active_thread_count

    @property
    def id(self):
        """
        Gets the id of this ProcessorStatusSnapshotDTO.
        The id of the processor.

        :return: The id of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProcessorStatusSnapshotDTO.
        The id of the processor.

        :param id: The id of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._id = id

    @property
    def group_id(self):
        """
        Gets the group_id of this ProcessorStatusSnapshotDTO.
        The id of the parent process group to which the processor belongs.

        :return: The group_id of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ProcessorStatusSnapshotDTO.
        The id of the parent process group to which the processor belongs.

        :param group_id: The group_id of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._group_id = group_id

    @property
    def name(self):
        """
        Gets the name of this ProcessorStatusSnapshotDTO.
        The name of the prcessor.

        :return: The name of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProcessorStatusSnapshotDTO.
        The name of the prcessor.

        :param name: The name of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this ProcessorStatusSnapshotDTO.
        The type of the processor.

        :return: The type of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ProcessorStatusSnapshotDTO.
        The type of the processor.

        :param type: The type of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._type = type

    @property
    def run_status(self):
        """
        Gets the run_status of this ProcessorStatusSnapshotDTO.
        The state of the processor.

        :return: The run_status of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._run_status

    @run_status.setter
    def run_status(self, run_status):
        """
        Sets the run_status of this ProcessorStatusSnapshotDTO.
        The state of the processor.

        :param run_status: The run_status of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        # case sensitive bug found in NiFi-1.2.0 - NiFi-1.4.0
        # allowed_values = ["RUNNING", "STOPPED", "DISABLED", "INVALID"]
        allowed_values = ["Running", "Stopped", "Disabled", "Invalid"]
        if run_status not in allowed_values:
            raise ValueError(
                "Invalid value for `run_status` ({0}), must be one of {1}"
                .format(run_status, allowed_values)
            )

        self._run_status = run_status

    @property
    def bytes_read(self):
        """
        Gets the bytes_read of this ProcessorStatusSnapshotDTO.
        The number of bytes read by this Processor in the last 5 mintues

        :return: The bytes_read of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_read

    @bytes_read.setter
    def bytes_read(self, bytes_read):
        """
        Sets the bytes_read of this ProcessorStatusSnapshotDTO.
        The number of bytes read by this Processor in the last 5 mintues

        :param bytes_read: The bytes_read of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._bytes_read = bytes_read

    @property
    def bytes_written(self):
        """
        Gets the bytes_written of this ProcessorStatusSnapshotDTO.
        The number of bytes written by this Processor in the last 5 minutes

        :return: The bytes_written of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_written

    @bytes_written.setter
    def bytes_written(self, bytes_written):
        """
        Sets the bytes_written of this ProcessorStatusSnapshotDTO.
        The number of bytes written by this Processor in the last 5 minutes

        :param bytes_written: The bytes_written of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._bytes_written = bytes_written

    @property
    def read(self):
        """
        Gets the read of this ProcessorStatusSnapshotDTO.
        The number of bytes read in the last 5 minutes.

        :return: The read of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._read

    @read.setter
    def read(self, read):
        """
        Sets the read of this ProcessorStatusSnapshotDTO.
        The number of bytes read in the last 5 minutes.

        :param read: The read of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._read = read

    @property
    def written(self):
        """
        Gets the written of this ProcessorStatusSnapshotDTO.
        The number of bytes written in the last 5 minutes.

        :return: The written of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._written

    @written.setter
    def written(self, written):
        """
        Sets the written of this ProcessorStatusSnapshotDTO.
        The number of bytes written in the last 5 minutes.

        :param written: The written of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._written = written

    @property
    def flow_files_in(self):
        """
        Gets the flow_files_in of this ProcessorStatusSnapshotDTO.
        The number of FlowFiles that have been accepted in the last 5 minutes

        :return: The flow_files_in of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_in

    @flow_files_in.setter
    def flow_files_in(self, flow_files_in):
        """
        Sets the flow_files_in of this ProcessorStatusSnapshotDTO.
        The number of FlowFiles that have been accepted in the last 5 minutes

        :param flow_files_in: The flow_files_in of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_in = flow_files_in

    @property
    def bytes_in(self):
        """
        Gets the bytes_in of this ProcessorStatusSnapshotDTO.
        The size of the FlowFiles that have been accepted in the last 5 minutes

        :return: The bytes_in of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_in

    @bytes_in.setter
    def bytes_in(self, bytes_in):
        """
        Sets the bytes_in of this ProcessorStatusSnapshotDTO.
        The size of the FlowFiles that have been accepted in the last 5 minutes

        :param bytes_in: The bytes_in of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._bytes_in = bytes_in

    @property
    def input(self):
        """
        Gets the input of this ProcessorStatusSnapshotDTO.
        The count/size of flowfiles that have been accepted in the last 5 minutes.

        :return: The input of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._input

    @input.setter
    def input(self, input):
        """
        Sets the input of this ProcessorStatusSnapshotDTO.
        The count/size of flowfiles that have been accepted in the last 5 minutes.

        :param input: The input of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._input = input

    @property
    def flow_files_out(self):
        """
        Gets the flow_files_out of this ProcessorStatusSnapshotDTO.
        The number of FlowFiles transferred to a Connection in the last 5 minutes

        :return: The flow_files_out of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_out

    @flow_files_out.setter
    def flow_files_out(self, flow_files_out):
        """
        Sets the flow_files_out of this ProcessorStatusSnapshotDTO.
        The number of FlowFiles transferred to a Connection in the last 5 minutes

        :param flow_files_out: The flow_files_out of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_out = flow_files_out

    @property
    def bytes_out(self):
        """
        Gets the bytes_out of this ProcessorStatusSnapshotDTO.
        The size of the FlowFiles transferred to a Connection in the last 5 minutes

        :return: The bytes_out of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_out

    @bytes_out.setter
    def bytes_out(self, bytes_out):
        """
        Sets the bytes_out of this ProcessorStatusSnapshotDTO.
        The size of the FlowFiles transferred to a Connection in the last 5 minutes

        :param bytes_out: The bytes_out of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._bytes_out = bytes_out

    @property
    def output(self):
        """
        Gets the output of this ProcessorStatusSnapshotDTO.
        The count/size of flowfiles that have been processed in the last 5 minutes.

        :return: The output of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._output

    @output.setter
    def output(self, output):
        """
        Sets the output of this ProcessorStatusSnapshotDTO.
        The count/size of flowfiles that have been processed in the last 5 minutes.

        :param output: The output of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._output = output

    @property
    def task_count(self):
        """
        Gets the task_count of this ProcessorStatusSnapshotDTO.
        The number of times this Processor has run in the last 5 minutes

        :return: The task_count of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._task_count

    @task_count.setter
    def task_count(self, task_count):
        """
        Sets the task_count of this ProcessorStatusSnapshotDTO.
        The number of times this Processor has run in the last 5 minutes

        :param task_count: The task_count of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._task_count = task_count

    @property
    def tasks_duration_nanos(self):
        """
        Gets the tasks_duration_nanos of this ProcessorStatusSnapshotDTO.
        The number of nanoseconds that this Processor has spent running in the last 5 minutes

        :return: The tasks_duration_nanos of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._tasks_duration_nanos

    @tasks_duration_nanos.setter
    def tasks_duration_nanos(self, tasks_duration_nanos):
        """
        Sets the tasks_duration_nanos of this ProcessorStatusSnapshotDTO.
        The number of nanoseconds that this Processor has spent running in the last 5 minutes

        :param tasks_duration_nanos: The tasks_duration_nanos of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._tasks_duration_nanos = tasks_duration_nanos

    @property
    def tasks(self):
        """
        Gets the tasks of this ProcessorStatusSnapshotDTO.
        The total number of task this connectable has completed over the last 5 minutes.

        :return: The tasks of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        """
        Sets the tasks of this ProcessorStatusSnapshotDTO.
        The total number of task this connectable has completed over the last 5 minutes.

        :param tasks: The tasks of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._tasks = tasks

    @property
    def tasks_duration(self):
        """
        Gets the tasks_duration of this ProcessorStatusSnapshotDTO.
        The total duration of all tasks for this connectable over the last 5 minutes.

        :return: The tasks_duration of this ProcessorStatusSnapshotDTO.
        :rtype: str
        """
        return self._tasks_duration

    @tasks_duration.setter
    def tasks_duration(self, tasks_duration):
        """
        Sets the tasks_duration of this ProcessorStatusSnapshotDTO.
        The total duration of all tasks for this connectable over the last 5 minutes.

        :param tasks_duration: The tasks_duration of this ProcessorStatusSnapshotDTO.
        :type: str
        """

        self._tasks_duration = tasks_duration

    @property
    def active_thread_count(self):
        """
        Gets the active_thread_count of this ProcessorStatusSnapshotDTO.
        The number of threads currently executing in the processor.

        :return: The active_thread_count of this ProcessorStatusSnapshotDTO.
        :rtype: int
        """
        return self._active_thread_count

    @active_thread_count.setter
    def active_thread_count(self, active_thread_count):
        """
        Sets the active_thread_count of this ProcessorStatusSnapshotDTO.
        The number of threads currently executing in the processor.

        :param active_thread_count: The active_thread_count of this ProcessorStatusSnapshotDTO.
        :type: int
        """

        self._active_thread_count = active_thread_count

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
        if not isinstance(other, ProcessorStatusSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
