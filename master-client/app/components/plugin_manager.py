#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import *

class PluginManager:
        plugins = {
            "dos": DDosAttack
        }