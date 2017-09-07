#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import traceback
import socket

from tornado.tcpserver import TCPServer
from tornado.gen import coroutine, Task, Return
from tornado.ioloop import IOLoop

from util import common
from pushconnection import PushConn
from pushserver_config import ListenPort

global logger
logger = common.install_logger(__name__)


class PushServer(TCPServer):

    """push server """

    def __init__(self):
        """TODO: to be defined1. """
        TCPServer.__init__(self)
        self._connecions = set()
        pass


    @coroutine
    def handle_stream(self, stream, address):
        logger.info('connected {0[0]} at {0[1]}'.format(address))
        conn = PushConn(stream, address)
        stream.set_close_callback(conn.on_close)
        conn._stream = stream
        r = yield conn.on_connect()

if __name__ == '__main__':
    logger.info('starting push server ...')
    server = PushServer()
    server.listen(ListenPort)

    IOLoop.instance().start()


