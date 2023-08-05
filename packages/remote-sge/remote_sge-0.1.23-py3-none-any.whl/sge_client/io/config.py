"""
    ============================
    Configuring your application
    ============================

    Both the client and the server can have a configuration file, although the
    server will basically work without it.  See `Config File Settings Reference`_
    for all your options.  Files are looked for in the following order, and each
    later file overwrites prior ones.

    * default config settings
    * ``/etc/remote_sge/config.ini``
    * ``$HOME/.config/remote_sge/config.ini``
    * ``$PWD/.remote_sge_config.ini``
    * finally, in the location pointed to by ``$REMOTE_SGE_CONFIG``

    Client config file needs to have the [client] section. ::

        [client]
        host = remote-sge-host
        port = 8080
        tunnel_port = 8085


    Server config can be empty but you might want the following sections: ::

        [qsub_settings]
        output_path=/place/where/output/files/go
        parallel_environment = smp 4

        [command_environment]
        ENVVAR1 = bav
        ENVVAR2 = quaz


    Config files are basic *ini* structure and are loaded by :mod:`configparser`.

    ==============================
    Config File Settings Reference
    ==============================

    [remote_sge]
    ^^^^^^^^^^^^

    shell
        Default: ``/bin/bash``.  The shell to use for calls to qsub_ and qstat_.

    [client]
    ^^^^^^^^

    host
        The name or ip address of the remote host to contact.

    port
        The remote port to contact for HTTP requests.  Default: 8080.

    tunnel_remote_bind_addr
        Default: ``127.0.0.1``.  The address on the remote host to which the
        tunnel will be bound.  *You probably don't want to change this.*

    tunnel_local_bind_addr
        Default: ``127.0.0.1``.  The address on the local host to which the
        tunnel will be bound.  *You probably don't want to change this.*

    tunnel_local_bind_port
        Default: ``8085``.  The port on the local host to which the tunnel
        will be bound.  Only needs to be changed if that port is reserved on
        your system.

    use_ssh_tunnel
        Default: ``yes``.  Only turn this off if you have your own plans for
        locking down the remote host.


    [command_environment]
    ^^^^^^^^^^^^^^^^^^^^^
    Any settings give here will be passed directly as environment variables to
    jobs running on the remote cluster.


    [qsub_settings]
    ^^^^^^^^^^^^^^^

    This config section describes the basic parameters that will be passed to
    qsub_.

    output_path
        The location on the execution host where SGE output files should be written.
        Default is nothing, in which case output files will be written to the
        working directory for each job.  This can get a little messy and can also
        result in the output files being scattered about.

    join_stdout_and_stderr
        Default: ``yes``.  Tells the execution host to write both output streams
        to a single file.

    command_shell
        The shell under which script jobs will be run. Default: ``/bin/bash``,
        which is valid on CentOS as well as Amazon Linux.

    parallel_environment
        The parallel environment specification.  Default is empty which means
        no parallel execution environment.  See to the ``-pe`` qsub_ option.

        Note that a four-slot job might be described differently from one system
        to another, for example on Rocks it should be ``orte 4`` whereas on
        cfncluster it should be ``smp 4``.


    binary_executable
        Default: ``no``.  See the ``-b`` qsub_ option.  You want this to stay as
        it is as long as you're sending script files over to the remote host for
        execution.

    default_queue
        Default: empty.  Allows the remote jobs to run within a given queue.

    exec_in_shell
        Default: ``yes``.  See the ``-shell`` qsub_ option.  Only included for
        completeness.  This setting has no effect unless ``binary_executable``
        is set to ``yes``.



    .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
    .. _qstat: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html

"""
from os.path import join, abspath, expanduser
from os import getenv, environ, getcwd
import site
import configparser
# import collections

#  Files are loaded in this order.
DEFAULT_CONFIG_PATH = 'etc/remote_sge/config.ini'
SYSTEM_CONFIG_PATH = '/etc/remote_sge/config.ini'
USER_CONFIG_PATH = '~/.config/remote_sge/config.ini'
CWD_CONFIG_PATH = '.remote_sge_config.ini'
CLIENT_CONF_ENVVAR = 'REMOTE_SGE_CONFIG'

def load_config():
    """
        Loads the application configuration files using the :mod:`configparser` module.

        Returns:
            :class:`~configparser.ConfigParser` object containing the aggregate settings
            from the files described in `Configuring your application`_.
    """
    files = [abspath(join(site.PREFIXES[0], DEFAULT_CONFIG_PATH)),
            SYSTEM_CONFIG_PATH,
             expanduser(USER_CONFIG_PATH),
             join(getcwd(), CWD_CONFIG_PATH)]
    if CLIENT_CONF_ENVVAR in environ:
        files.insert(0, abspath(getenv(CLIENT_CONF_ENVVAR)))
    parser = configparser.ConfigParser()
    print(parser.read(files))
    return parser



# CONFIG = configure_app_config()
# CLIENT_CONFIG = CONFIG['client']
# if CONFIG.has_section('server'):
#     SERVER_CONFIG = CONFIG['server']
#     QSUB_SETTINGS = CONFIG['qsub_settings']
#     QSUB_PARAMETERS = collections.OrderedDict(CONFIG['qsub_parameters'])
#     COMMAND_ENVIRONMENT = collections.OrderedDict(CONFIG['command_environment'])

