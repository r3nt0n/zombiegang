#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import os

class Config(object):
    DEBUG = True
    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.getcwd()
    APP_DIR = os.path.join(BASE_DIR, 'app/')
    DATA_DIR = os.path.join(APP_DIR, 'data/')
    TEMP_DIR = os.path.join(DATA_DIR, 'tmp/')

    # used for CSRF protection in wtf-forms (hidden_tag)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # comment second condition in PRD
    # future use to local authentication operations required (enable/disable proxy)
