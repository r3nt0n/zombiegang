#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import zession

from app.models.data import Data


class Mission(Data):
    def __init__(self):
        super().__init__()
        self.name = 'mission'
        self.task_id = ''
        self.zombie_username = ''
        self.read_confirm = ''
        self.running = ''
        self.result = ''
        self.exec_at = ''

    def create(self, data=None):
        # subclasses method runs here...
        if data is None:
            data = {}
        if 'task_id' in data:
            self.task_id = data['task_id']
        if 'zombie_username' in data:
            self.zombie_username = data['zombie_username']

        return Data.create(self, data)