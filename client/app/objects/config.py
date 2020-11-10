#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import os

class Config:
    DEBUG = True
    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.getcwd()
    APP_DIR = os.path.join(BASE_DIR, 'app/')
    DATA_DIR = os.path.join(APP_DIR, 'data/')
    TEMP_DIR = os.path.join(DATA_DIR, 'tmp/')

