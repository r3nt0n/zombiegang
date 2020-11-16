#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from . import http_client, machine

from app.modules.attacks.ddos.slowloris import Slowloris
from .logger import Logger

from app import config
config = config.Config()
logger = Logger(debug=config.DEBUG)
logger.start()