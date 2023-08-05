#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import falcon
from gevent import pywsgi
from gevent import socket
from gevent.pool import Pool
from wishbone_input_httpserver.middleware import GenerateMetaData
from wishbone_input_httpserver.middleware import BasicAuthentication
from wishbone_input_httpserver.middleware import TokenAuthentication
from wishbone_input_httpserver.middleware import Authorize
from wishbone_input_httpserver.middleware import DeriveQueue
from wishbone.error import QueueMissing, ProtocolError


class LogWrapper(object):

    def __init__(self, wishbone_logger):

        self.logging = wishbone_logger

    def write(self, data):

        self.logging.info(data.rstrip())


class EventHandler(object):

    def __init__(self, decoder, wishbone_event_callback):

        self.decoder = decoder
        self.wishbone_event_callback = wishbone_event_callback

    def on_get(self, req, resp, queue="outbox"):

        try:
            response = self.wishbone_event_callback("", req.meta, req.queue)
        except QueueMissing as err:
            resp.status = falcon.HTTP_404
            resp.body = str(err)
        else:
            resp.body = response

    def on_put(self, req, resp, queue="outbox"):

        try:
            for chunk in self.decoder(req.stream):
                resp.body = self.wishbone_event_callback(chunk, req.meta, req.queue)
        except QueueMissing as err:
            resp.status = falcon.HTTP_404
            resp.body = str(err)
        except ProtocolError as err:
            resp.status = falcon.HTTP_406
            resp.body = "There was an error processing your request. Reason: %s" % str(err)

    on_post = on_put


class FalconServer(object):

    def __init__(self, address, port, ssl_key, ssl_cert, ssl_cacerts, poolsize, so_reuseport,
                 wishbone_event_callback, wishbone_logger, wishbone_decoder, wishbone_queues,
                 callback_authorize_user, callback_authorize_token, callback_get_password_hash, callback_requires_authentication):

        self.address = address
        self.port = port
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.ssl_cacerts = ssl_cacerts
        self.poolsize = poolsize
        self.so_reuseport = so_reuseport
        self.wishbone_event_callback = wishbone_event_callback
        self.logger = wishbone_logger
        self.wishbone_decoder = wishbone_decoder
        self.wishbone_queues = wishbone_queues

        self.app = falcon.API(
            middleware=[
                DeriveQueue(
                    wishbone_queues
                ),
                BasicAuthentication(
                    callback_get_password_hash
                ),
                TokenAuthentication(
                ),
                Authorize(
                    callback_authorize_user,
                    callback_authorize_token,
                    callback_requires_authentication
                ),
                GenerateMetaData(
                )
            ]
        )

        event_handler = EventHandler(
            wishbone_decoder,
            wishbone_event_callback
        )

        self.app.add_route('/{queue}', event_handler)
        # self.app.add_sink(self.handle_404, '')

        if self.ssl_key is not None and self.ssl_cert is not None:
            ssl_options = {
                "keyfile": self.ssl_key,
                "certfile": self.ssl_cert,
                "ca_certs": self.ssl_cacerts
            }
        else:
            ssl_options = {}

        self.server = pywsgi.WSGIServer(
            listener=self.__getListener(),
            application=self.app,
            spawn=Pool(self.poolsize),
            log=LogWrapper(self.logger),
            error_log=None,
            **ssl_options
        )

    def start(self):
        self.server.start()

    def handle_404(self, req, resp):
        resp.status = falcon.HTTP_404
        message = "Queue '%s' does not exist. Event dropped." % (req.path)
        resp.body = message
        self.logger.error(message)

    def stop(self):
        self.server.stop()

    def __getListener(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.so_reuseport:
            sock.setsockopt(socket.SOL_SOCKET, 15, 1)

        sock.setblocking(0)
        sock.bind((self.address, self.port))
        sock.listen(50)
        return sock
