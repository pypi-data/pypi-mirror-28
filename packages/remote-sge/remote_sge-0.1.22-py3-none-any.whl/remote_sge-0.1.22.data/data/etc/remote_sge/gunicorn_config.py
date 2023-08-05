"""
# Gunicorn only cares about the variables set at the very bottom of the file.
# Restful SGE Client settings can also be provided at the time of object creation.

"""
from os.path import dirname, join, abspath

#########################################################
#
#                 gunicorn settings
#
#########################################################

# Name of the gunicorn instance
name = "restful_sge"
# IP or socket binding
bind = "${wsgi_binding}"
# User whom gunicorn will run as
user="$$USER"
# Group whom gunicorn will run as
group="$$USER"
# Number of worker processes to start
workers=4

pythonpath="/var/remote_sge"

# Location of the logging config file.  Don't change this, probably.
logconfig = "${dest_path}/logging.conf"
