import os
import configparser
import sys
import string
from string import Template
from os.path import join, abspath, expandvars
from tempfile import NamedTemporaryFile

from argparse import RawTextHelpFormatter
from sge.util.arg_parser import ArgParser

YUM_PACKAGES = ['nginx', 'sqlite-devel', 'readline-devel', 'bzip2-devel',
                'git', 'gcc', 'gcc-c++', 'kernel-devel', 'make',
                'zlib-devel', 'openssl-devel']

CONFIG_DIR = "%s/etc/remote_sge" % sys.prefix
# CONFIG_DIR = '/var/remote_sge/etc'
CONFIG = {
    'editor' : None,
    'use_sudo' : False
}
DEFAULT_EDITOR = 'vim'
DESCRIPTION = """SGE Server Installer.

This script will make changes to your system, a number of which require
sudo priveleges.  Be warned.

You'll be prompted to edit/view configuration files created.  Make sure that
your editor of choice is properly configured.  See -e option for detail.

if the -i option is given, the following changes will be made to your system:

    * You'll be prompted to modify / verify various configuration settings.
    * nginx server will be configured as a proxy for the wsgi server.
    * It will NOT change existing nginx configuration, so if you want
        to turn off the default nginx server you'll have to do that yourself.
    * An upstart script will be installed, to control the wsgi server.
    * A certificate authority and self-signed server key will be created.

if -a is given, script YUM will be invoked to install nginx sqlite-devel
    readline-devel bzip2-devel git gcc gcc-c++ kernel-devel make zlib-devel
    openssl-devel
"""


ALINUX_ARG_TEXT = """Amazon Linux only, installs requirements via YUM.
Installs the following: nginx sqlite-devel readline-devel bzip2-devel
git gcc gcc-c++ kernel-devel make zlib-devel openssl-devel

This is enough to ensure that Python will build without warnings, and
that C extensions for required libraries will all compile.

TODO: verify that there are no unneeded dependencies listed here.
"""

EDITOR_TEXT = """Select an editor, such as pico.  Defaults to vim,
unless $EDITOR is set. If $EDITOR is set then this
option can be omitted, but specifying -e will overwrite
the settings from $EDITOR.
"""

ROOT_DESCRIPTION = """Where to place configs. Defaults to "$HOME/.config/remote_sge".
The main readon for changing this would be if you want place
the configuration into /etc/remote_sge.

Be sure that you take note of the access controls on whatever
location you specify.  If writing to that location requires
sudo privileges, be sure to specify the -s parameter."""

SYSTEMD_HELP = """Specify this if your system uses systemd.  Otherwise upstart will
be assumed.  This affects how gunicorn is installed, and how the
installer will restart services."""

FINAL_MESSAGE = """\n*\n*\n*\n********    FINISHED!!    **********\n
Installation seems to be successful.

You'll want to do a final check using test_remote_sge_server utility which is provided
to you, just to ensure connectivity.

I've packaged your client certificates into $HOME/remote_sge_client_certs.tgz.
Please copy that file to your client machine, you'll need them for client setup.

Now, ssh to the client machine, and begin there.  Toodles!

"""

def sudo(command):
    os.system("sudo %s" % command)

def maybe_sudo(command):
    print(command)
    if CONFIG['use_sudo']:
        sudo(command)
    else:
        os.system(command)

parser = ArgParser(prog="remote_sge",
                   formatter_class=RawTextHelpFormatter)

def get_editor(args):
    if args.editor:
        return args.editor
    elif 'EDITOR' in os.environ:
        return os.environ['EDITOR']
    else:
        return DEFAULT_EDITOR

def edit_config_file(name, filename, dest=None, **substitutions):
    source = join(CONFIG_DIR, filename)
    if dest:
        substitutions['dest_path']=expandvars(dest)
    with NamedTemporaryFile(mode='w') as temp_file:
        template = string.Template(open(source).read())
        temp_file.write(expandvars(template.substitute(**substitutions)))
        temp_file.flush()
        print("Press enter to edit %s in your favorite editor." % name)
        sys.stdin.flush()
        sys.stdin.read(1)
        os.system(CONFIG['editor'] + " " + temp_file.name)
        if dest:
            maybe_sudo("cp " + temp_file.name + " " + join(dest, filename))
        else:
            return open(temp_file.name).read()


def parse_args():
    parser.description = """
    Installs a working remote SGE server component.
    """
    parser.add_argument('install_server', help='Command.')
    parser.add_argument('-e', '--editor', help=EDITOR_TEXT, default=None)
    parser.add_argument('-i', '--install',
                        help="Perform the installation.",
                        action="store_true")
    parser.add_argument('-r', '--root',
                        help=ROOT_DESCRIPTION,
                        default="$HOME/.config/remote_sge")
    parser.add_argument('-s', '--sudo',
                        help="Use sudo for placing config files (e.g. if installing into /etc).",
                        action="store_true")
    parser.add_argument('-a', '--alinux',
                        help="""Installs system components on Amazon Linux.""",
                        action="store_true")
    parser.add_argument('--systemd',
                        help=SYSTEMD_HELP,
                        action="store_true")
    parser.description = DESCRIPTION
    return parser.parse_args()

class SslKeyCommands(object):
    CREATE_CA_KEY="openssl genrsa ${enctype} -out ${certs_path}/ca.key 4096"
    CREATE_CA_CRT=("openssl req -new -x509 -days 365 -key ${certs_path}/ca.key" +
                   " -out ${certs_path}/ca.crt -subj " +
                   "\"/C=${country_code}/ST=${state}/L=${city}/O=${org}" +
                   "/OU=${org_unit}/CN=${common_name}\"")
    CREATE_SERVER_KEY="openssl genrsa ${enctype} -out ${certs_path}/server.key 1024"
    CREATE_SERVER_CSR=("openssl req -new -key ${certs_path}/server.key " +
                       "-out ${certs_path}/server.csr -subj " +
                       "\"/C=${country_code}/ST=${state}/L=${city}/O=${org}" +
                       "/OU=${org_unit}/CN=${common_name}\"")
    SELF_SIGNED_TLS_CERT=("openssl x509 -req -days 365 -in ${certs_path}/server.csr " +
                          "-CA ${certs_path}/ca.crt -CAkey ${certs_path}/ca.key " + 
                          "-set_serial 01 -out ${certs_path}/server.crt")
    CREATE_CLIENT_KEY="openssl genrsa ${enctype} -out ${certs_path}/client.key 1024"
    CREATE_CLIENT_CSR=("openssl req -new -key ${certs_path}/client.key "+
                       "-out ${certs_path}/client.csr -subj " + 
                       "\"/emailAddress=${email}/C=${country_code}/ST=${state}" +
                       "/L=${city}/O=${org}/OU=${org_unit}/CN=${name}\"")
    SIGN_CLIENT_CERT=("openssl x509 -req -days 365 -in ${certs_path}/client.csr " +
                      "-CA ${certs_path}/ca.crt -CAkey ${certs_path}/ca.key " +
                      "-set_serial 01 -out ${certs_path}/client.crt")

def install_keys(args):
    certs_path = join(args.root, 'certs')
    maybe_sudo("mkdir -p %s" % certs_path)
    ssl_config = load_config(string=edit_config_file("SSL Certificate details", 'ssl_config.ini'),
                             name='ssl')
    def make_key(template, message):
        print("Creating " + message)
        maybe_sudo(Template(template).substitute(certs_path=certs_path, **ssl_config['ssl']))
    make_key(SslKeyCommands.CREATE_CA_KEY, "Certificate  authority key")
    make_key(SslKeyCommands.CREATE_CA_CRT, "Certificate authority certificate")
    make_key(SslKeyCommands.CREATE_SERVER_KEY, "Private key for server")
    make_key(SslKeyCommands.CREATE_SERVER_CSR, "CSR for server certificate")
    make_key(SslKeyCommands.SELF_SIGNED_TLS_CERT, "Self-signed server certificate")
    make_key(SslKeyCommands.CREATE_CLIENT_KEY, "Client key")
    make_key(SslKeyCommands.CREATE_CLIENT_CSR, "Client certificate request")
    make_key(SslKeyCommands.SIGN_CLIENT_CERT, "Client certificate signed by our own CA")
    print("\n\nOkay, I placed all your certificates in " + certs_path)

def load_config(file=None, string=None, name=None):
    config = configparser.ConfigParser()
    if file:
        print("loading " + file)
        config.read(expandvars(file))
        print(config.sections())
    if string:
        config.read_string(string)
    if name:
        CONFIG[name] = config
    return config

def setup_gunicorn(args):
    os.system("$HOME/.pyenv/versions/remote_sge/bin/pip install flask gunicorn")
    edit_config_file("Gunicorn Config File", "gunicorn_config.py", args.root, **CONFIG['main']['server'])
    edit_config_file("Gunicorn Upstart Config", "gunicorn_upstart.conf", args.root, **CONFIG['main']['server'])
    edit_config_file("Gunicorn Logging Config", "logging.conf", args.root, **CONFIG['main']['server'])
    sudo("ln -s %s /etc/init/remote_sge_wsgi.conf" % expandvars(join(args.root, "gunicorn_upstart.conf")))
    sudo("ln -s /var/remote_sge/bin/gunicorn_init.d.sh /etc/init.d/remote_sge")

def do_install(args):
    CONFIG['editor'] = get_editor(args)
    if args.alinux:
        sudo("yum -y install " + " ".join(YUM_PACKAGES))
    maybe_sudo("mkdir -p %s" % args.root)
    edit_config_file("Main config file", "config.ini", args.root)
    config = load_config(file=join(args.root, "config.ini"), name="main")
    install_keys(args)
    edit_config_file("Web Server Configuration", "nginx.conf", args.root, **config['server'])
    sudo("ln -s %s /etc/nginx/conf.d/remote_sge.server.conf" % expandvars(join(args.root, "nginx.conf")))
    sudo("usermod -aG $USER nginx")
    restart_service('nginx')
    setup_gunicorn(args)
    os.system("tar -cvzf $HOME/remote_sge_client_certs.tgz %s/client.key %s/client.crt 1> /dev/null")
    print(FINAL_MESSAGE)

def restart_service(name):
    print("Restarting " + name)
    if CONFIG['loader'] == 'upstart':
        command = "service %s restart"
    else:
        command = "systemctl restart %s"
    sudo(command % name)

def set_system_loader(args):
    if args.systemd:
        CONFIG['loader'] = 'systemd'
    else:
        CONFIG['loader'] = 'upstart'

def main():
    args = parse_args()
    set_system_loader(args)
    if args.sudo:
        CONFIG['use_sudo'] = True
    if args.install:
        do_install(args)
    else:
        parser.print_help()
        exit(1)

if __name__ == '__main__':
    main()


