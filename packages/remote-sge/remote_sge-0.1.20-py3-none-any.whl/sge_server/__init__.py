"""
Main entry point into application, called by flask executable, gunicorn or wsgi plugin
for Apache or nginx.

There is a circular import here.  Here in the root of the :mod:`sge_server` package,
we declare ``app`` which is the one instance of the flask application object.  Then
we go on to import :mod:`sge_server.flask_views`.  The latter will in turn import the
``app`` object from this point in the namespace.

This pattern is recommended in the Flask docs under the heading of `Larger Applications`_.


.. _`Larger Applications`: http://flask.pocoo.org/docs/0.12/patterns/packages/



"""
# from os.path import isdir, expanduser, join
from flask import Flask
# from .config import SERVER_CONFIG

# if not isdir(SERVER_CONFIG.get('work_root')) or not isdir(SERVER_CONFIG.get('completed_files_root')):
#     raise ValueError("Check config file and ensure that work_root and completed_files_root exist.")

app = Flask(__name__)

import sge_server.flask_views

# if SERVER_CONFIG.get('job_wrapper'):
#     import restful_sge.job_submission_control
#     restful_sge.job_submission_control.JOB_WRAPPER = SERVER_CONFIG.get('job_wrapper')

