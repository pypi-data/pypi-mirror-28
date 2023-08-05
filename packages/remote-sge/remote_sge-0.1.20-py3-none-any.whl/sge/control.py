"""
Functions to control the queue status of a given job.
"""
import os.path
import subprocess

QDEL = os.path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qdel")
QHOLD = os.path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qhold")
QMOD = os.path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qmod")
QALTER = os.path.expandvars("${SGE_ROOT}/bin/${SGE_ARCH}/qalter")

class QModOpt(object):
    SUSPEND = r'-sj'
    UNSUSPEND = r'-usj'

RESULT_PATTERN = "has deleted job %s"

def terminate(job_id):
    """
    calls qdel_ with the given job id.  Boolean return value indicates successful response.

    **Will only work for jobs owned by the calling user.**

    .. _qdel: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qdel.html
    """
    process = subprocess.run([QDEL, str(job_id)])
    return process.returncode == 0

def user_hold(job_id):
    """
    Calls qhold_ for the given job id, placing a *user hold* on the job.

    **NOTE:** Because it's a user hold being placed, it's possible that even an operator
    might get access denied trying to hold jobs owned by another user.  This will have
    to be sussed out.

    .. _qhold: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qhold.html

    """
    process = subprocess.run([QHOLD, str(job_id)])
    return process.returncode == 0

def suspend(job_id):
    """
    Calls qmod_ for the given job id, suspending the running job.

    User must have the appropriate privilege to accomplish this.

    .. _qmod: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qmod.html

    """
    process = subprocess.run([QMOD, QModOpt.SUSPEND, str(job_id)])
    return process.returncode == 0

def resume(job_id):
    """
    Calls qmod_ for the given job id, resuming the suspended job.

    User must have the appropriate privilege to accomplish this.

    .. _qmod: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qmod.html

    """
    process = subprocess.run([QMOD, QModOpt.UNSUSPEND, str(job_id)])
    return process.returncode == 0


def remove_user_hold(job_id):
    """
    Calls qalter_ to remove a user hold from a job.

    .. _qalter: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qalter.html

    """
    process = subprocess.run([QALTER, '-h', 'U', str(job_id)])
    return process.returncode == 0
