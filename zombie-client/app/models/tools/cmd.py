#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

class Command(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.result = ''


    def start(self):
        # here comes the sugar
        from app.components import logger, machine
        commands = self.task_content
        if commands:
            if ";" in commands:
                command_list = commands.split(";")
            else:
                command_list = [commands]
            for command in command_list:
                logger.log('executing {}'.format(command))
                machine.execute_comand(command)
                if type(machine.output) == bytes:
                    machine.output = machine.output.decode('utf-8')
                if machine.output:
                    self.result += machine.output
                logger.log('cmd executed: {}'.format(command), 'SUCCESS')

    def run(self):
        return Task.run(self)
