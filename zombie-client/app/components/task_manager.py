#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import queue, threading
from datetime import datetime
from time import sleep

from app.components import config, logger, scheduler
from app.models import *
from app.modules import crud


class TaskManager:
    def __init__(self):
        self.new_tasks = queue.Queue()
        self.completed_tasks = queue.Queue()

    def merge_mission_task_data(self, task_data, mission_data):
        task = {}
        for k in task_data:
            task[k] = task_data[k]
        task['id'] = mission_data['task_id']
        task['mission_id'] = mission_data['id']
        task['read_confirm'] = mission_data['read_confirm']
        task['result'] = mission_data['result']
        task['running'] = mission_data['running']
        task['exec_at'] = mission_data['exec_at']
        task['mission_manual_stop'] = mission_data['manual_stop']
        return task

    def get_new_tasks(self):
        # load scheduled tasks (it only loads those which exists in cc, marked as read and wasnt executed yet)
        scheduler.load_scheduled_tasks()
        # add scheduled tasks to new_tasks queue (this is done only one time) it forces to remove executed tasks
        # from file, because the file is rewritten again in do_task with loaded sch_tasks one by one
        [self.new_tasks.put(loaded_task) for loaded_task in (list(scheduler.tasks.queue)) if
         loaded_task.mission_id not in [t.mission_id for t in (list(self.new_tasks.queue))]]

        while True:
            new_missions = crud.read_data('missions', {'read_confirm': 'false'})
            if new_missions and (new_missions != 'any found'):
                logger.log('new_homework: {}'.format(len(new_missions)), 'SUCCESS')
                for mission in new_missions:
                    response = crud.read_data('tasks', {'mission_id': mission['id'],
                                                        'id': mission['task_id']})

                    if response:
                        # prepare fields to task data model
                        task_data = response[0]
                        task_data = self.merge_mission_task_data(task_data, mission)
                        # create new task object
                        task = Task(task_data)

                        # update read confirm
                        if not task.report_is_read():
                            logger.log('error trying to update read confirm on cc for {}'.format(task), 'ERROR')
                            continue
                        logger.log('read confirm updated for {}'.format(task), 'SUCCESS')

                        # add new task object to execution queue
                        self.new_tasks.put(task)
                        #logger.log(list(self.new_tasks.queue), 'INFO')
            else:
                logger.log('any new task received', 'INFO')

            self.check_scheduled_tasks()
            sleep(config.read_setting('refresh_tasks'))

    def post_completed_tasks(self):
        while True:
            task = self.completed_tasks.get()
            logger.log('trying to post task exec result: {}'.format(task, 'OTHER'))
            # if crud.update_data('mission',{
            #     "id": task.mission_id,
            #     "result": task.result,
            #     "exec_at": task.exec_at}):
            #     self.completed_tasks.task_done()
            #     logger.log('{} task exec result successfully posted'.format(task, 'SUCCESS'))
            if task.report_result():
                self.completed_tasks.task_done()
                logger.log('{} task exec result successfully posted'.format(task, 'SUCCESS'))


    def check_scheduled_tasks(self):
        qeue_original_size = len(list(scheduler.tasks.queue))
        for x in range(0, qeue_original_size):
            sch_task = scheduler.tasks.get()
            logger.log('checking execution time for scheduled task {}'.format(sch_task), 'OTHER')
            # logger.log('execution_time {}'.format(sch_task.to_exec_at), 'OTHER')
            # logger.log('execution_time {}'.format(datetime.now() <= datetime.strptime(sch_task.to_exec_at, '%Y-%m-%d %H:%M:%S')), 'OTHER')
            if datetime.now() >= datetime.strptime(sch_task.to_exec_at, '%Y-%m-%d %H:%M:%S'):
                self.new_tasks.put(sch_task)
                logger.log('scheduled task {} has reach execution time, added to tasks queue and removed from scheduler'.format(sch_task),'SUCCESS')
                scheduler.tasks.task_done()
            else:
                scheduler.tasks.put(sch_task)

    def keep_doing_new_tasks(self):
        while True:
            task = self.new_tasks.get()
            if self.do_task(task):
                self.completed_tasks.put(task)
                logger.log('task {} completed'.format(task), 'SUCCESS')
            self.new_tasks.task_done()

    def do_task(self, task):
        from app.components import plugin_manager
        Plugin = plugin_manager.get_plugin(task.task_type)
        if Plugin and task.task_content:
            # convert task object into a dict to create a new object with extended fields
            task_data = {}
            for attr, value in task.__dict__.items():
                task_data[attr] = value
            task = Plugin(task_data)

            # execute task
            if datetime.now() >= datetime.strptime(task.to_exec_at, '%Y-%m-%d %H:%M:%S'):

                thread_manual_stop = threading.Thread(name='manual_stop', target=task.keep_reading_manual_stop)#, args=((task,)))
                thread_run_task = threading.Thread(name='run_task', target=task.run)

                thread_manual_stop.start()
                executed = thread_run_task.start()
                # executed = task.run()

                thread_manual_stop.join()
                thread_run_task.join()

                if executed:
                    output = task.result
                return True

            # schedule task for future execution
            elif task not in list(scheduler.tasks.queue):
                scheduler.add_task(task)
                logger.log('task {} added to scheduler'.format(task), 'INFO')
                logger.log('scheduler.tasks: {}'.format(list(scheduler.tasks.queue)), 'OTHER')
                return False



