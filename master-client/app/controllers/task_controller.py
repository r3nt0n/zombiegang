#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import logger

from app.modules.plugins import get_plugin

from app.models import *


class TaskController:
    def __init__(self, task_type):
        self.error = None
        self.created = []
        self.task_data = {}
        self.zombies_data = {}
        self.last_created_task = None
        self.last_created_mission = None

        self.TaskModel = get_plugin(task_type)

    def get_zombies_data(self):
        from app.controllers import DataFilter
        zombies_filter = DataFilter('zombies')
        zombies_filter.run()
        if zombies_filter.data:
            self.zombies_data = zombies_filter.data

    def run(self, task_data=None, selected_zombies=None):
        task = self.TaskModel()
        mission = Mission()
        if task.create(task_data):
            self.last_created_task = task
            mission.task_id = task.id
            logger.log('task created, trying to create mission for each zombie selected...', 'DEBUG')
            for zombie in selected_zombies:
                mission.zombie_username = zombie
                if mission.create():
                    self.created.append(zombie)
                    self.last_created_mission = mission
                    logger.log('mission for {} created'.format(zombie), 'DEBUG')
                else:
                    logger.log('error trying to create mission for zombie {}'.format(zombie), 'ERROR')
                    continue
            logger.log('{} missions created'.format(len(self.created)), 'DEBUG')
            return True
        else:
            logger.log('error trying to create task, task data: {}'.format(task_data), 'ERROR')
            self.error = 'error trying to create task, already exists'
            return False
