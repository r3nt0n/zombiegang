#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from app import config
config = config.Config()

from app.components.logger import Logger
logger = Logger(debug=config.DEBUG)
logger.start()

from app.components.machine import Machine
machine = Machine()

from app.components.token import Token
token = Token()

from app.components.scheduler import Scheduler
scheduler = Scheduler(config.PATH_SCHEDULER)

from app.components.task_manager import TaskManager
task_manager = TaskManager()

from app.components.plugin_manager import PluginManager
plugin_manager = PluginManager()
