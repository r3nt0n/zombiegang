#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app.models import Task

from app.modules.attacks import Bruteforcer


class BruteForceAttack(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        # here unpack values inside task_content
        self.target = self.task_content['target']
        self.attack_type = self.task_content['attack_type']
        self.slice_wl = self.task_content['slice_wl']
        self.usernames_wl = self.task_content['usernames_wl']
        self.passwords_wl = self.task_content['passwords_wl']
        self.combined_wl = self.task_content['combined_wl']
        from app.components import logger
        logger.log(self.target, 'DEBUG')
        logger.log(self.attack_type, 'DEBUG')
        logger.log(self.slice_wl, 'DEBUG')
        logger.log(self.usernames_wl, 'DEBUG')
        logger.log(self.passwords_wl, 'DEBUG')
        logger.log(self.combined_wl, 'DEBUG')

    def start(self):
        # here comes the sugar
        from app.components import logger
        logger.log('starting bruteforce module...', 'OTHER')

        #if self.attack_type == 'ssh':
        attack = Bruteforcer(self.attack_type, self.target, to_stop_at=self.to_stop_at, port=23, n_sockets=1000,
                             slice_wl=self.slice_wl, wordlists={'usernames': self.usernames_wl,
                                                                'passwords': self.passwords_wl,
                                                                'combined': self.combined_wl})
        attack.run()
        logger.log('bruteforcer executed', 'OTHER')
        self.result = attack.report
        Task.start(self)
        # ...
        # return ...


    def run(self):
        return Task.run(self)

