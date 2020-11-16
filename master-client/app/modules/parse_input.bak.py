#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import logger


def merge_values(date_value, time_value):
    if date_value is None:
        date_value = ''
    if time_value is None:
        time_value = ''
    return ((date_value + ' ' + time_value).rstrip()).lstrip()






def parse_input_create_attack(request):
    if (request.method == 'POST') and ('create_btn' in request.form):
        task_data = {}
        selected_zombies = []

        # task content
        task_content = {}
        if request.form.get('target'):
            task_content['target'] = request.form.get('target')
        if request.form.get('attack_type'):
            task_content['attack_type'] = request.form.get('attack_type')
        if request.form.get('wordlist'):
            task_content['wordlist'] = request.form.get('wordlist')

        if task_content:
            task_data['task_content'] = task_content

        # to exec at
        if request.form.get('to_exec_at_date') or request.form.get('to_exec_at_time'):
            task_data['to_exec_at'] = merge_values(request.form.get('to_exec_at_date'),
                                                             request.form.get('to_exec_at_time'))

        # to stop at
        if request.form.get('to_stop_at_date') or request.form.get('to_stop_at_time'):
            task_data['to_stop_at'] = merge_values(request.form.get('to_stop_at_date'),
                                                             request.form.get('to_stop_at_time'))

        # selected_zombies
        if request.form.getlist('zombies_checked'):
            selected_zombies = request.form.getlist('zombies_checked')

        return selected_zombies, task_data

    return False

