from typing import Tuple, List, Type, Set
from logging import getLogger, Logger
import socket
import camel_case_switcher.dict_processor
import copy

from http_server_base.empty_request_handler import Empty_RequestHandler
from http_server_base.health_check_request_handler import HealthCheck_RequestHandler
from http_server_base.tools.config_loader import ConfigLoader

from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

class _Protocols:
    __http = 'http'
    __https = 'https'
    
    http = __http
    HTTP = __http
    
    https = __https
    HTTPS = __https

class HttpServerBase(Application):
    """
    HttpServerBase class.
    Actually, it is child for tornado.web.Application class, and generates tornado.httpserver.HTTPServer only during the `run` command.
    
    The following attributes can be overrided:
    :attribute logger_name
    :attribute handlers
    List of handlers those are passed to the to tornado.web.Application class during the initialisation.
    If untouched (None or missing), default handlers will be used.
    """
    
    logger_name:str = 'http_server'
    handlers:List[Tuple[str, Type[RequestHandler]]]
    
    default_handlers = \
    [
        (r"^/?$", Empty_RequestHandler, dict(redirect_page='/static/index.html')),
        (r"^/healthcheck(|(/.*))$", HealthCheck_RequestHandler),
    ]
    
    __logger: Logger = None
    __server: HTTPServer = None
    
    __self_addr: str = None
    __listen_port: int = None
    __protocol:str = None
    
    def __init__(self,
            config_name:str='main', config_prefix='HTTP', config_priority=False,
            **settings):
        """
        Initializes a new instance of tornado.web.Application and prepares tornado.httpserver.HTTPServer to be run.

        :param config_name:
        Name of config in the ConfigLoader class, where the settings are loaded from.
        By default, settings are loaded from the main config.
        :param config_prefix:
        Prefix part of the config path to the server's settings. Path keys are '/'-separated.
        Note that due to the implementation's restrictions, server settings could not be in the top-level of the config.
        :param config_priority:
        By default, arguments passed directly to the initializer, have more priority.
        By setting config_config_priority=True, you are prioritising config over the keyword arguments.
        
        
        :param settings:
        Keyword arguments. Partially parsed by HttpServerBase, partially passed to the tornado.web.Application
        All HttpServerBase optional parameters are listed below.
        Note that all CamelCase parameters loaded from the config would be morphed into the underscore_style,
            so `selfAddress` and `ListenPort` are completely legal.
        
        :param self_address:
        str. Hardcoded server uri. Used only for the info message about server start and several responses based on the `self_address` property.
        Should contain protocol.
        :param listen_ip:
        str. Used only if `self_address` is not set up for the `self_address` calculation.
        If missing as well, server will try to self-discover.
        The resulting self_address will have protocol - http or https, ip-address and, if custom, a port.
        :param ip:
        Same as `listen_ip`.
        :param listen_port:
        int value of port, which server is uses to listen requests.
        By default 80 or 443 port is used - according to the SSL configuration
        :param port:
        Same as `listen_port`.
        
        :param SSL
        NOT IMPLEMENTED YET
        
        dict. Group of parameters required for SSL.
        Any of them can be passed directly as an argument as well.
        """

        self.__logger = getLogger(self.logger_name)
        
        if ((not hasattr(self, 'handlers')) or (self.handlers is None)):
            self.handlers = HttpServerBase.default_handlers
            self.logger.debug("Using default handlers")
        else:
            self.logger.debug(f"List of handlers: {self.handlers}")
        
        _settings = camel_case_switcher.dict_processor.dict_keys_camel_case_to_underscope(ConfigLoader.get_from_config(config_prefix, config_name=config_name, default=lambda: dict()))
        if (config_priority):
            settings_deep_copy = copy.deepcopy(settings)
            settings_deep_copy.update(_settings)
            _settings = settings_deep_copy
        else:
            _settings.update(settings)
        
        _ssl = None
        # _ssl = _settings.get('SSL')
        if (_ssl):
            protocol = _Protocols.HTTPS
        else:
            protocol = _Protocols.HTTP
        
        listen_port = _settings.get('port')
        if (listen_port is None):
            if (protocol == _Protocols.HTTP):
                listen_port = 80
            elif (protocol == _Protocols.HTTPS):
                listen_port = 443
            listen_port_part = ""
        else:
            listen_port_part = f":{listen_port}"
        
        self_address = _settings.get('self_address')
        if (self_address):
            pass
        else:
            listen_address = \
                _settings.get('listen_address') \
                or _settings.get('listen_ip') \
                or _settings.get('ip') \
                or socket.gethostbyname(socket.gethostname()) \
            ;
            self_address = f"{protocol}://{listen_address}{listen_port_part}"

        super().__init__(handlers=self.handlers, **_settings)
        self.__self_addr = self_address
        self.__listen_port = listen_port
    
    @classmethod
    def __self_discover_generator(cls):
        names = \
        [
            'localhost',
            socket.getfqdn(),
        ]
        for name in names:
            try:
                for _value in cls.__self_discover_generator_per_interface(name=name):
                    yield _value
            except socket.herror:
                continue

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_addr = s.getsockname()[0]
        try:
            for _value in cls.__self_discover_generator_per_interface(addr=local_addr):
                yield _value
        except socket.herror:
            pass
    
    @classmethod
    def __self_discover_generator_per_interface(cls, name=None, addr=None):
        if (addr is None):
            assert not name is None, "Either name or addr is required"
            addr = socket.gethostbyname(name)
        yield addr
        _name, _alias_list, _address_list = socket.gethostbyaddr(addr)
        yield _name
        for _alias in _alias_list:
            yield _alias
        for addr in _address_list:
            yield addr
            yield socket.getfqdn(_name)
            yield socket.gethostbyname(_name)
    
    @classmethod
    def self_discover(cls) -> Set[str]:
        """
        Server will try to do some self-discovery job.
        Not used in the distributed version.
        
        :return:
        The result is non-sorted set of unique items which could be associated with the local host.
        Usually it looks like:
        { '127.0.0.1', '127.0.1.1', 'localhost', 'MyComputer', '192.168.0.14' }
        """
        
        return set(cls.__self_discover_generator())
    
    @property
    def logger(self) -> Logger:
        return self.__logger
    
    @property
    def self_address(self) -> str:
        """
        Returns the self_address value, which was calculated during the initialisation process.
        :return:
        Returns self_address value.
        """
        
        return self.__self_addr

    def run(self):
        """
        Runs the server on the port specified earlier.
        Server blocks the IO.
        """
        
        self.logger.info("Starting HTTP service...")

        self.__server = HTTPServer(self)
        self.__server.listen(self.__listen_port)
        self.logger.info("Service started")
        self.logger.info(f"Listnening on the {self.self_address}.")
        IOLoop.current().start()
