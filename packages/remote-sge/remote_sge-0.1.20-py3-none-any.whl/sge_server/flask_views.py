"Entry point for Restful SGE API Server"
import json
from time import sleep
from os.path import isfile, join, abspath
from flask import request, make_response, send_from_directory, redirect
# from restful_sge.qsub_wrapper import QSubWrapper
# from restful_sge.job_detail import get_job_detail, get_job_list
# from .config import SERVER_CONFIG
from sge_server import app

# def job_file(job_id):
#     path = abspath(join(SERVER_CONFIG.get('completed_files_root'), '%s.tgz' % job_id))
#     if isfile(path):
#         return path

@app.route("/")
def root_path():
    "Root path"
    return json.dumps({
            'status': 200,
            'application': "Remote SGE",
            'message' : "Unauthorized use is forbiddden."
        })

# @app.route("/jobs.json")
# def jobs_json():
#     "Get list of all current jobs."
#     return json.dumps(get_job_list())

# @app.route("/queues/<queue_id>/jobs.json")
# def jobs_json_by_queue(queue_id):
#     "JSON data for all jobs in queue"
#     return json.dumps(get_job_list(queue_id))

# @app.route("/jobs/<job_id>.json")
# def get_job_json(job_id):
#     "Detailed JSON data for the given job."
#     detail = get_job_detail(job_id)
#     if detail:
#         response = json.dumps(detail)
#     elif job_file(job_id):
#         response = redirect(job_file(job_id), code=301)
#     else:
#         response = make_response("{}", 404)
#     return response

# @app.route("/jobs/<job_id>.tgz")
# def get_job_archive(job_id):
#     "Detailed JSON data for the given job."
#     return send_from_directory(SERVER_CONFIG.get('completed_files_root'), "%s.tgz" % job_id)

@app.route('/jobs', methods=['POST'])
def submit_job():
    "Post job data and submit job to SGE."
    if 'file' in request.files:
        fileobj = request.files['file']
    else:
        fileobj = None

    with QSubWrapper.remote_job(request.form.get('name'),
                                request.form.get('command'),
                                work_root=SERVER_CONFIG.get('work_root'),
                                finished_archive_dir=SERVER_CONFIG.get('completed_files_root'),
                                command_arguments=request.form.getlist('arguments'),
                                fileobj=fileobj)  as job_control:
        job_control.submit()
        sleep(0.01)
        detail = job_control.get_job_detail()
        return make_response(json.dumps(detail), 202)
