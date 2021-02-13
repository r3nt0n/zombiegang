#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models.data import Data


class Task(Data):
    def __init__(self, task_type='cmd'):
        super().__init__()
        self.name = 'task'
        self.task_name = ''
        self.task_type = task_type
        self.task_content = {}
        self.master_username = ''
        self.to_exec_at = ''
        self.to_stop_at = ''

    def create(self, data=None):
        # subclasses method runs here...

        # base task fields
        from app import zession
        self.master_username = zession.username

        if data:
            if 'task_name' in data:
                self.task_name = data['task_name']

            if ('to_exec_at_date' in data) or ('to_exec_at_time' in data):
                if not 'to_exec_at_date' in data: data['to_exec_at_date'] = None
                if not 'to_exec_at_time' in data: data['to_exec_at_time'] = None
                self.to_exec_at = self.merge_values(data['to_exec_at_date'], data['to_exec_at_time'])

            if ('to_stop_at_date' in data) or ('to_stop_at_time' in data):
                if not 'to_stop_at_date' in data: data['to_stop_at_date'] = None
                if not 'to_stop_at_time' in data: data['to_stop_at_time'] = None
                self.to_stop_at = self.merge_values(data['to_stop_at_date'], data['to_stop_at_time'])

            # task content (only if it wasn't set before by a subclass)
            if (not self.task_content) and 'task_content' in data:
                self.task_content = data['task_content']

        # packing task content
        #self.task_content = self.pack_value(self.task_content)

        return Data.create(self, data)


class Command(Task):
    def __init__(self):
        super().__init__('cmd')
    def create(self, data=None):
        # subclasses method runs here...
        return Task.create(self, data)


class RemoteShellSession(Task):
    def __init__(self):
        super().__init__('rsh')
    def create(self, data=None):
        # subclasses method runs here...
        return Task.create(self, data)