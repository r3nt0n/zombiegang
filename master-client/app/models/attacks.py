#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from .tasks import Task


class BaseAttack(Task):
    def __init__(self, task_type):
        super().__init__()
        self.task_type = task_type

    def create(self, data=None):
        # subclasses method runs here...
        if 'target' in data:
            self.task_content['target'] = data['target']
        if 'attack_type' in data:
            self.task_content['attack_type'] = data['attack_type']

        return Task.create(self, data)


class DDosAttack(BaseAttack):
    def __init__(self):
        super().__init__('dos')


class BruteForceAttack(BaseAttack):
    def __init__(self):
        super().__init__('brt')

    def create(self, data=None):
        # task content
        if 'wordlist'in data:
            self.task_content['wordlist'] = data['wordlist']

        return BaseAttack.create(self, data)

