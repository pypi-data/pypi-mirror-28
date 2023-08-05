"""
Thin client for making shell commands out to qstat.

All calls return the raw XML given by the qstat command
"""
from subprocess import run, PIPE
from re import findall
from os import getenv
# from drmaa import Session as DrmaaSession
# from drmaa.errors import InvalidJobException


def qstat(arg_string):
    """
    Runs qstat inside of the user's shell and returns the STDOUT output from the command.

    Args:
        arg_string (str): the arguments to be passed to the qstat command.

    Returns:
        stringified stdout output from qstat command.
    """
    command = [getenv('SHELL'), '-c', 'qstat %s' % arg_string]
    return run(command, stdout=PIPE).stdout.decode()

def get_job_detail(job_id):
    """
    Returns an XML object representing the current state of the given job.
    XML returned is exactly what was returned from the **qstat** command.

    Args:
        job_id (str): the ID of the job within the cluster being queried.

    Returns:
        The raw XML for the current job state.  
        
        Note that current versions of
        qstat tend to return invalid XML if job is not found.  Clients must search
        for the string "unknown_jobs" in order to determine that the job was not found.

        Currently published schemata for qstat do not correctly describe what is actually
        returned by the command.  See a reference implementation for the transformation,
        elsewhere in this project.




    """
    return qstat('-u "*" -j %s -xml' % job_id)
    # if findall("unknown_jobs", xml):
    #     return None
    # else:
    #     job_detail = parse_job_detail(xml)[0]
    #     return dict(state=get_job_state(job_id, session), **job_detail)

def get_job_list(queue=None):
    if queue:
        queue = '-q %s' % queue
    return qstat('%s -u "%s" -xml' % (queue or '', getenv('USER')))
    # return parse_job_list(xml)
