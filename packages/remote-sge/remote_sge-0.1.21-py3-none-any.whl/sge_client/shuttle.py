"""
Plumbing for sending the local job to the remote.

Ultimately, a request needs to be sent to the server, with:

* job_name
* arguments
* job_files


"""
from os.path import basename
import requests
import sge.control
import sge.status
from sge_client.io.jobarchive import package_job

def send_job_to_remote(job_id):
    """
    Packages the job and sends it to the remote server.
    """
    sge.control.user_hold(job_id)
    job_detail = sge.status.get_job_detail(job_id)

    requests.post('http://remote-sge.getsandbox.com/jobs.json', json={
        'name' : job_detail.job_name,
        'command' : basename(job_detail.command_path),
        'arguments' : job_detail.arguments,
        'environment' : job_detail.environment,
        'package' : package_job(job_detail.command_path)
    })
