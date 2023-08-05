"For obtaining the status of a job"
from os import path
from xml.etree import ElementTree
import re
import sge.shell
from sge.helpers import (XPathAttr, IntConverter, XmlEnvironmentDeserializer,
                         XmlJobArgumentsDeserializer, XmlIntDeserializer)

QSTAT = path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qstat")
STATE_PATTERN = re.compile(r"^.{40}(\w+)")

class SgeJobStateCode(object):
    "Job state codes as returned by qstat."
    SUSPENDED = r's'
    RUNNING = r'r'
    QUEUED_ACTIVE = r'qw'
    QUEUED_HELD = r'hqw'
    UNKNOWN = r'unknown'


def get_job_status(job_id):
    """
    Calls qstat_ and parses the output for the state of the job.

    Returns:
        a state code from :class:`~sge.status.SgeJobStateCode`

    .. _qstat: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html
    """
    output = sge.shell.run_in_shell(r"%s | grep -e '^\s*%s'" % (QSTAT, job_id))
    match = STATE_PATTERN.match(output)
    if match:
        return match[1]
    else:
        return SgeJobStateCode.UNKNOWN


class JobDetail(object):
    """
    Receives an XML ElementTree and provides attributes which read from it.

    
    """
    command_path = XPathAttr('JB_script_file')
    owner = XPathAttr('JB_owner')
    job_id = XPathAttr('JB_job_number', XmlIntDeserializer)
    uid = XPathAttr('JB_uid', XmlIntDeserializer)
    gid = XPathAttr('JB_gid', XmlIntDeserializer)
    job_name = XPathAttr('JB_job_name')
    environment = XPathAttr('JB_env_list', XmlEnvironmentDeserializer)
    arguments = XPathAttr('JB_job_args', XmlJobArgumentsDeserializer)

    def __init__(self, xml_node):
        self.xml_node = xml_node

    def to_dict(self):
        "Makes it into a dictionary"
        return dict(command_path=self.command_path, owner=self.owner, job_id=self.job_id,
                    uid=self.uid, gid=self.gid, job_name=self.job_name,
                    environment=self.environment, arguments=self.arguments)


def get_job_detail(job_id):
    """
    Retrieves the XML output from qstat_ and parses it.

    .. _qstat: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html
    """
    xml = sge.shell.run(QSTAT, '-j', str(job_id), '-xml')
    if re.findall('unknown_jobs', xml):
        return None
    else:
        root = ElementTree.fromstring(xml)
        return JobDetail(root.find('djob_info/element'))
