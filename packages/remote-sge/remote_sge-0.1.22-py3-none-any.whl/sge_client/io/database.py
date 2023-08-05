"""
    Basic file storage for a JSON object.
"""
from os.path import expanduser
from json import loads, dumps
from datetime import datetime
from filelock import FileLock

DBFILE = expanduser('~/.sge_client.db.json')
LOCKFILE = expanduser('~/.sge_client.lock')

R_ID = 'remote_job_id'
L_ID = 'local_job_id'

def initialize():
    "Initializes a new empty data file.  Overwrites the current file, if one exists."
    with open(DBFILE, 'w') as file:
        file.write(dumps([]))

class Db(object):
    """
        Basic file storage for a JSON object.
    """
    def where_not_in(self, column, *values):
        """
        Selects results which do not match the given column/values expression.

        Args:
            column (str): The named field to test against.

            values (str): Vales to search for.  A record will not be returned if the field named
                in *column* is contained inside of the list of values given.
        """
        return [x for x in self.data if x[column] not in values]

    def all_jobs(self):
        "Retrieve all records."
        return self.data

    def values(self):
        "Synonym for #all_jobs."
        return self.data

    def find_by_remote_job_id(self, job_id):
        """
        Finds a record by the id number for that job on the remote cluster.

        Args:
            job_id(str): the job id for this job as scheduled or running on the remote.

        Returns:
            A :class:`dict` object containing various attributes of the job on the local and the remote::

                {  
                    local_id: '123123',
                    local_state: 3,
                    local_wd: '/var/sge_working_dir',
                    remote_id: '1234324',
                    remote_state: 2,
                    remote_wd: '/var/remote_working_dir',
                    last_checked: '2017-12-27 16:35:30.898984'
                }
        
        """
        return next((x for x in self.values() if x[R_ID] == job_id), None)

    def find_by_local_job_id(self, job_id):
        
        return next((x for x in self.values() if x[L_ID] == job_id), None)

    def insert(self, local_id, local_state, local_wd, remote_id, remote_state, remote_wd):
        self.data.append(dict(local_id=local_id,
                              local_state=local_state,
                              local_wd=local_wd,
                              remote_id=remote_id,
                              remote_state=remote_state,
                              remote_wd=remote_wd,
                              last_checked=str(datetime.now())))

    def update(self, job):
        job['last_checked'] = str(datetime.now())

    def delete(self, job):
        return self.data.remove(job)

    def __init__(self):
        self.lock = FileLock(LOCKFILE)
        self.data = None

    def save(self):
        with open(DBFILE, 'w') as file:
            file.write(dumps(self.data))

    def open(self):
        self.lock.acquire(timeout=2)
        with open(DBFILE) as file:
            self.data = loads(file.read())
        
    def close(self):
        self.save()
        self.data = None
        self.lock.release()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, x, y, z):
        "Exit method for resource"
        self.close()
