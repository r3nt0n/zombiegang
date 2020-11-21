#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

class RemoteShellSession(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.toggle = self.task_content

    def start(self):
        from app.components import logger, config
        logger.log('remote shell session: {}'.format(self.toggle), 'QUESTION')
        if self.toggle == 'on':
            old_refresh_time = config.enable_rshell_session()
            self.result = old_refresh_time
        else:
            config.disable_rshell_session()

    def run(self):
        return Task.run(self)
