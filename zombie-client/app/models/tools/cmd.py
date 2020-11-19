#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

class Command(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.command = self.task_content['command']


    def start(self):
        # here comes the sugar
        from app.components import logger
        logger.log('executing cmd: {}'.format(self.command), 'QUESTION')
        # ...
        pass

    def run(self):
        return Task.run(self)
