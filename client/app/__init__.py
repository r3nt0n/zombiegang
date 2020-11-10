#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

from app.objects import Config
config = Config

from app.objects import Logger
logger = Logger(debug=config.DEBUG)
logger.start()
logger.set_level(logger.console_handler, 'DEBUG')
# logger.set_level(logger.console_handler, 'INFO')
logger.log('starting app', level='DEBUG')

from app.objects import Zession
zession = Zession()
from app.objects import Buffer
buffer = Buffer()
from app.objects import Proxy
proxy = Proxy()
#proxy.get_socks5_session('127.0.0.1', 9050)
#from app.modules import http_client

from app import routes
