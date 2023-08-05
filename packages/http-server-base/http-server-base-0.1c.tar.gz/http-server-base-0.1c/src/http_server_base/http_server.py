from typing import Tuple, List, Type

from http_server_base.empty_request_handler import Empty_RequestHandler
from http_server_base.health_check_request_handler import HealthCheck_RequestHandler

from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import socket
from http_server_base.tools.config_loader import ConfigLoader
from logging import getLogger, Logger

class HttpServerBase(Application):
    
    logger_name:str = 'http_server'
    handlers:List[Tuple[str, Type[RequestHandler]]] = \
    [
        (r"^/?$", Empty_RequestHandler, dict(redirect_page='/static/index.html')),
        (r"^/healthcheck(|(/.*))$", HealthCheck_RequestHandler),
    ] \
    ;
    
    __logger: Logger = None
    __server: HTTPServer = None
    __self_addr: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(handlers=self.handlers, *args, **kwargs, static_path=ConfigLoader.get_from_config('HTTP/staticFiles'))
        self.__logger = getLogger(self.logger_name)
        self.__server = HTTPServer(self)
        self.__self_addr = 'http://{ip}:{port}'.format(ip=socket.gethostbyname(socket.gethostname()), port=ConfigLoader.get_from_config('HTTP/port'))

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def self_address(self) -> str:
        return self.__self_addr

    @property
    def self_address(self) -> str:
        return self.__self_addr

    def run(self):
        self.logger.info('Starting HTTP service...')
    
        self.__server.listen(ConfigLoader.get_from_config('HTTP/port'))
        self.logger.info('Service started')
        IOLoop.current().start()
