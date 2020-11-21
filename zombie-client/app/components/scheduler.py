#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import queue

from app.modules import crud
from app.components import logger
from app.models.task import Task
from app.modules.backup_settings import get_zombie_settings, set_zombie_settings

class Scheduler:
    def __init__(self, path):
        self.tasks = queue.Queue()
        self.db_file_path = path
        self.reg_name = 'schtasks'

    # read saved conf from winreg/file
    def load_scheduled_tasks(self):
        loaded_tasks = get_zombie_settings(self.db_file_path, self.reg_name)
        logger.log('loaded tasks: {}'.format(loaded_tasks), 'DEBUG')
        if loaded_tasks:
            for load_task_data in loaded_tasks:
                # check that loaded task also exists in cc and is already marked as read
                response = crud.read_data('missions', {"id": load_task_data["mission_id"]})
                if (response and ("read_confirm" in response[0]) and (response[0]["read_confirm"] == "true")
                        and not (response[0]["result"])):
                    for sch_task in list(self.tasks.queue):
                        if sch_task.mission_id == load_task_data["mission_id"]:
                            continue
                    self.tasks.put(Task(load_task_data))
            return True
        return False

    # write running conf to winreg/file
    def write_scheduled_tasks(self):
        try:
            tasks = list(self.tasks.queue)
            tasks_list = []
            for task_object in tasks:
                task_dict = {}
                for attr, value in task_object.__dict__.items():
                    #if value:  # save even empty values
                    task_dict[attr] = value
                if task_dict:
                    tasks_list.append(task_dict)

            if set_zombie_settings(self.db_file_path, self.reg_name, tasks_list):
                return True
        except Exception as e:
            logger.log(e, 'CRITICAL')
            return False

    def add_task(self, task_object):
        #self.tasks.put(task_object)
        if task_object.mission_id not in [sch_task.mission_id for sch_task in (list(self.tasks.queue))]:
            self.tasks.put(task_object)
        self.write_scheduled_tasks()
