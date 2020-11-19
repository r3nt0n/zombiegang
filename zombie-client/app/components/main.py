#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import sys
import threading

from app import zombie
from app.components import logger


class Brain:
    def __init__(self):
        pass

    def think_as_a_zombie(self):
        def keep_logged_in(zombie):
            zombie.keep_logged_in()

        def get_new_tasks(zombie):
            zombie.get_new_tasks()

        def keep_doing_new_tasks(zombie):
            zombie.keep_doing_new_tasks()

        def post_completed_tasks(zombie):
            zombie.post_completed_tasks()


        while True:
            threads = []
            try:
                if zombie.run():

                    thread_keep_logged_in = threading.Thread(name='keep_logged_in', target=keep_logged_in, args=((zombie,)))
                    threads.append(thread_keep_logged_in)

                    thread_get_new_tasks = threading.Thread(name='get_new_tasks', target=get_new_tasks, args=((zombie,)))
                    threads.append(thread_get_new_tasks)

                    thread_keep_doing_new_tasks = threading.Thread(name='keep_doing_new_tasks', target=keep_doing_new_tasks, args=((zombie,)))
                    threads.append(thread_keep_doing_new_tasks)

                    thread_post_completed_tasks = threading.Thread(name='post_completed_tasks', target=post_completed_tasks, args=((zombie,)))
                    threads.append(thread_post_completed_tasks)

                    # Start all threads
                    for t in threads:
                        # t.setDaemon(True)
                        t.start()

                    # Wait for all of them to finish
                    for t in threads:
                        t.join()

            except KeyboardInterrupt:
                logger.log('manual exit requested \n\nPRESS Ctrl+C again...', 'CRITICAL')
                break

            except Exception as e:
                logger.log('CRITICAL ERROR: {}'.format(e), 'CRITICAL')
                logger.log('trying to restart connection', 'INFO')
                continue

