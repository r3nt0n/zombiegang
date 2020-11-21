#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

class Command(Task):
    def __init__(self, task_data):
        super().__init__(task_data)


    def start(self):
        # here comes the sugar
        from app.components import logger, machine
        command = self.task_content
        if command:
            machine.execute_comand(command)
            if machine.output:
                self.result = (machine.output).decode('utf-8')
        logger.log('cmd executed: {}'.format(command), 'SUCCESS')

    def run(self):
        return Task.run(self)
