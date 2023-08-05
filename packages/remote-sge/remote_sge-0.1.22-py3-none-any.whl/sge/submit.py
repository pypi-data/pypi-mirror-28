"For submitting jobs through qsub"
from os import path
import re
from sge.helpers import (DictionaryConverter, DateTimeConverter,
                         BoolConverter, CmdOptionAttr)
import sge.shell

JOB_ID_REGEX = r"job (\d+) \("
QSUB = path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qsub")

class JobSubmissionState(object):
    HOLD_STATE = "hold"
    ACTIVE_STATE = "active"


class QSubOptions(object):
    HOLD = '-h'
    WORKING_DIR = '-wd'
    START_TIME = '-a'
    JOB_NAME = '-N'
    ENV = '-v'
    OUTPUT_PATH = '-o'
    JOIN = '-j'
    SHELL = '-S'
    PARALLEL_ENVIRONMENT = '-pe'
    BINARY = '-b'
    EXEC_IN_SHELL = '-shell'
    QUEUE = '-q'
    DEADLINE_TIME = '-dl'

class JobRequest(object):
    """
    A request for a new job, which is submitted to qsub_ via the
    :func:`sge.submit.JobRequest.submit` method.

    At a very minimum, the `command_path` must be set or else no job
    will be submitted.

    .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
    """

    def submit(self):
        """
        Submits the given job request by calling out to qsub.

        Args:
            job_template (`~sge.submit.JobRequest`): An object describing the requested job.

        Returns:
            The ID of the new job, as an integer.

            If no job was successfully submitted, returns None.
        """
        qsub_arguments = [*[y for x in self.qsub_options.items() for y in x if y],
                          self.command_path, *self.command_arguments]
        cmd_output = sge.shell.run(QSUB, *qsub_arguments)
        matches = re.findall(JOB_ID_REGEX, cmd_output)
        if matches:
            return int(matches[0])

    command_path = None
    """The command to be executed."""

    @property
    def job_submission_state(self):
        """
        Whether the job should be submitted with a hold, or queued/active.
        Use the constants from :class:`drmaa.JobSubmissionState`.
        """
        if QSubOptions.HOLD in self.qsub_options:
            return JobSubmissionState.HOLD_STATE
        else:
            return JobSubmissionState.ACTIVE_STATE

    @job_submission_state.setter
    def job_submission_state(self, value):
        """
        Since -h is a binary flag, setting the value here will either add or remove
        the flag from `qsub_options`.
        """
        if value == JobSubmissionState.HOLD_STATE:
            self.qsub_options[QSubOptions.HOLD] = None
        elif QSubOptions.HOLD in self.qsub_options:
            del self.qsub_options[QSubOptions.HOLD]


    working_directory = CmdOptionAttr(QSubOptions.WORKING_DIR)
    native_specification = None #: Raw command-line options for qsub.
    start_time = CmdOptionAttr(QSubOptions.START_TIME, DateTimeConverter)#: Start time
    job_name = CmdOptionAttr(QSubOptions.JOB_NAME)
    output_path = CmdOptionAttr(QSubOptions.OUTPUT_PATH)
    join_files = CmdOptionAttr(QSubOptions.JOIN, BoolConverter)
    deadline_time = CmdOptionAttr(QSubOptions.DEADLINE_TIME, DateTimeConverter)
    command_arguments = [] #: The arguments to be given to the command.
    environment = CmdOptionAttr(QSubOptions.ENV, DictionaryConverter)

    def __init__(self, **kwargs):
        """
        Builds a JobTemplate instance.

        Attributes can be passed as keyword arguments.
        """
        self.qsub_options = {}
        for aname in kwargs:
            setattr(self, aname, kwargs.get(aname))

