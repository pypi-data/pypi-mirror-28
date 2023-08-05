"""
Responsible for filesystem IO associated with packaging and unpacking
SGE jobs.
"""
from tempfile import SpooledTemporaryFile
from os.path import basename, join
from io import BytesIO
import glob
import re
import tarfile
from base64 import b64decode, b64encode

UTF8 = r"utf-8"

def extract_job(data, destination):
    """
    Receives a readable stream containing a tgz archive and extracts it to the given destination.

    Args:
        iobase (:class:`io.IOBase`): a readable IOBase object to extract.  Note that this
            is the base class of the :class:`~urllib3.response.HTTPResponse` class,
            which is given by the ``raw`` attribute of the :class:`~requests.models.Response`
            returned by :func:`~requests.get`.
        destination (str): filesystem location in which to extract the archive.
            Path must exist and be writable by this process
    Returns:
        None
    """
    with tarfile.open(mode="r|gz", fileobj=BytesIO(b64decode(data))) as archive:
        archive.extractall(destination)

def package_job(*individual_files, working_dir=None, mask="*"):
    """
    Receives a specification of files and returns a string containing a Base64-encoded, gzipped
    tarfile, containing the specified files.

    If the inputs for the remote command (or even the command itself) are not present in the 
    remote system, it is necessary to package the required data for submission to the remote.

    Files specified via *individual_files* parameter will be placed in the root path inside
    the archive.  Files inside of *working_dir* will retain their same path relative to
    *working_dir*.
    
    Args:
        individual_files: a list of :class:`str` representing complete paths to specific
            files to add to the archive.  These files will have their entire path stripped and
            will be added to the root path of the
            archive.  *please note that no care is taken to ensure against name collisions.*

        working_dir (:class:`str`): string path to the directory containing files to be archived.

        mask (:class:`str`): selector.  If working_dir is given, files in that directory will be
            included if they match the pattern given here.

    Returns: a string containing a Base64-encoded gzipped tarfile.
    """
    file_object = SpooledTemporaryFile()
    with tarfile.open(mode='x:gz', fileobj=file_object) as archive:
        for pathname in individual_files:
            archive.add(pathname, arcname=basename(pathname))
        if working_dir:
            filespec = join(working_dir, mask)
            relative_path_pattern = re.compile(r'%s(.*)$' % working_dir)
            for file in glob.glob(filespec, recursive=True):
                path_match = relative_path_pattern.match(file)
                if path_match:
                    archive.add(file, arcname=path_match[1])
    file_object.seek(0)
    return b64encode(file_object.read()).decode(UTF8)
