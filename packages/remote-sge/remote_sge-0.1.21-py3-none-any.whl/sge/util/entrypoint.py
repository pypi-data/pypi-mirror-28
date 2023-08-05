"""
Console entrypoint for various features:

* Client-Side Installer (remote_sge install_client)
* Server-Side Installer (remote_sge install_server)
"""
from argparse import ArgumentParser, RawTextHelpFormatter, REMAINDER
from sge_client.util.install import main as install_client
from sge_server.util.install import main as install_server
from sge_server.util.test_server import main as test_server

COMMAND_TEXT = """Available commands are:

install_server - Installs server components.
test_server    - Sends a request to verify that SSL, 
                 nginx, and Gunicorn are all configured.

For additional help, type "remote_sge <command>" with no args.
"""

def main():
    parser = ArgumentParser(prog="remote_sge: command utility for Remote SGE",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', help=COMMAND_TEXT)
    parser.add_argument('args', nargs=REMAINDER)
    args = parser.parse_args()
    if args.command == 'install_client':
        install_client()
    elif args.command == 'install_server':
        install_server()
    elif args.command == 'test_server':
        test_server()

if __name__ == '__main__':
    main()
