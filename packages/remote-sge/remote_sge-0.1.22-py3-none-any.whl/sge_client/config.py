"Configuration classes"

class Sections(object):
    "Sections"
    GENERAL = r'general'
    CLIENT = r'client'
    QSUB_SETTINGS = r'qsub_settings'
    QSUB_PARAMS = r'qsub_parameters'
    ENVIRONMENT = r'command_environment'

class Settings(object):
    "Settings"
    SHELL = r'shell'
    HOST = r'host'
    PORT = r'port'
    TUNNEL_REMOTE_BIND_ADDR = r'tunnel_remote_bind_addr'
    TUNNEL_LOCAL_BIND_ADDR = r'tunnel_local_bind_addr'
    TUNNEL_LOCAL_BIND_PORT = r'tunnel_local_bind_port'
    USE_SSH_TUNNEL = r'use_ssh_tunnel'

class Defaults(object):
    "Defaults"
    SHELL = r'/bin/bash'
    HOST = r'remote-sge-host'
    PORT = 8080
    TUNNEL_REMOTE_BIND_ADDR = r'127.0.0.1'
    TUNNEL_LOCAL_BIND_ADDR = r'127.0.0.1'
    TUNNEL_LOCAL_BIND_PORT = 8085
    USE_SSH_TUNNEL = True


class ConfigBase(object):
    "Config Base"


    def __init__(self, configparser):
        """
        Args:
            configparser (:class:`configparser.ConfigParser`): configuration settings.
        """
        self.general_settings = configparser[Sections.GENERAL]

    def shell(self):
        "The shell to use for calls to qsub and qstat."
        return self.general_settings.get(Settings.SHELL, Defaults.SHELL)

class ServerConfig(ConfigBase):
    "Server App Configuration"
    def __init__(self, configparser):
        """
        Args:
            configparser (:class:`configparser.ConfigParser`): configuration settings.
        """

        super().__init__(configparser)
        self.qsub_settings = configparser[Sections.QSUB_SETTINGS]
        self.__qsub_params = configparser[Sections.QSUB_PARAMS]
        self.__script_env = configparser[Sections.ENVIRONMENT]


    @property
    def qsub_parameters(self):
        """
        Returns a dictionary of default 

        """
        pass



class ClientConfig(ConfigBase):
    "Client App Configuration"
    def __init__(self, configparser):
        """
        Args:
            configparser (:class:`configparser.ConfigParser`): configuration settings.
        """

        super().__init__(configparser)
        self.client_settings = configparser[Sections.CLIENT]

    @property
    def host(self):
        "Host"
        return self.client_settings.get(Settings.HOST, Defaults.HOST)

    @property
    def port(self):
        "Port"
        return self.client_settings.getint(Settings.PORT, Defaults.PORT)

    @property
    def tunnel_remote_bind_addr(self):
        "tunnel remote bind address"
        return self.client_settings.get(Settings.TUNNEL_REMOTE_BIND_ADDR,
                                        Defaults.TUNNEL_REMOTE_BIND_ADDR)

    @property
    def tunnel_local_bind_addr(self):
        "Tunnel local bind address"
        return self.client_settings.get(Settings.TUNNEL_LOCAL_BIND_ADDR,
                                        Defaults.TUNNEL_LOCAL_BIND_ADDR)

    @property
    def tunnel_local_bind_port(self):
        "Tunnel local bind port"
        return self.client_settings.getint(Settings.TUNNEL_LOCAL_BIND_PORT,
                                           Defaults.TUNNEL_LOCAL_BIND_PORT)

    @property
    def use_ssh_tunnel(self):
        "Use SSH Tunnel"
        return self.client_settings.getboolean(Settings.USE_SSH_TUNNEL,
                                               Defaults.USE_SSH_TUNNEL)


